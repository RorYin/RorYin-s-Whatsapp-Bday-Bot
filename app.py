import os
from datetime import timedelta
from functools import wraps

from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)

from config import TEMP_DIR, get_settings, public_settings, save_settings
from gencard import generate_birthday_card
from greenapiwrapper import test_whatsapp_connection
from handler import run_daily_tasks
from people import add_person, delete_person, load_people, update_person

app = Flask(__name__)
app.secret_key = get_settings()["secret_key"]
app.permanent_session_lifetime = timedelta(hours=8)


def _role_from_password(password):
    settings = get_settings()
    if password == settings["superadmin_password"]:
        return "superadmin"
    if password == settings["admin_password"]:
        return "admin"
    return None


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "role" not in session:
            if request.path.startswith("/api/"):
                return jsonify({"ok": False, "error": "Login required."}), 401
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def superadmin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("role") != "superadmin":
            return jsonify({"ok": False, "error": "Superadmin access required."}), 403
        return view(*args, **kwargs)

    return wrapped


@app.context_processor
def inject_role():
    return {"role": session.get("role"), "is_superadmin": session.get("role") == "superadmin"}


@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if "role" in session:
            return redirect(url_for("dashboard"))
        return render_template("login.html", error=None)

    password = (request.form.get("password") or "").strip()
    role = _role_from_password(password)
    if not role:
        return render_template("login.html", error="Incorrect password.")
    session.permanent = True
    session["role"] = role
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/main")
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/api/me")
@login_required
def api_me():
    return jsonify({"ok": True, "role": session["role"]})


@app.route("/api/people", methods=["GET"])
@login_required
def api_people():
    people = load_people()
    return jsonify({"ok": True, "people": people, "count": len(people)})


@app.route("/api/people", methods=["POST"])
@login_required
def api_add_person():
    settings = get_settings()
    try:
        person, index = add_person(
            request.get_json(force=True) or {},
            settings["default_chatid"],
            settings["display_image_url"],
        )
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    return jsonify({"ok": True, "person": person, "index": index})


@app.route("/api/people/<int:index>", methods=["PUT"])
@login_required
def api_update_person(index):
    settings = get_settings()
    try:
        person = update_person(
            index,
            request.get_json(force=True) or {},
            settings["default_chatid"],
            settings["display_image_url"],
        )
    except IndexError:
        return jsonify({"ok": False, "error": "Person not found."}), 404
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400
    return jsonify({"ok": True, "person": person})


@app.route("/api/people/<int:index>", methods=["DELETE"])
@login_required
def api_delete_person(index):
    try:
        removed = delete_person(index)
    except IndexError:
        return jsonify({"ok": False, "error": "Person not found."}), 404
    return jsonify({"ok": True, "removed": removed})


@app.route("/api/actions/run-task", methods=["POST"])
@login_required
def api_run_task():
    payload = request.get_json(silent=True) or {}
    if not payload.get("confirmed"):
        return jsonify({"ok": False, "error": "Confirmation is required."}), 400
    try:
        log = run_daily_tasks()
        return jsonify({"ok": True, "log": log})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc), "log": []}), 500


@app.route("/api/actions/test-whatsapp", methods=["POST"])
@login_required
def api_test_whatsapp():
    payload = request.get_json(silent=True) or {}
    if not payload.get("confirmed"):
        return jsonify({"ok": False, "error": "Confirmation is required."}), 400
    try:
        card_path = generate_birthday_card("RorYinBoT")
        response = test_whatsapp_connection(card_path)
        ok = "Success" in str(response)
        return jsonify({"ok": ok, "result": str(response)})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/api/settings", methods=["GET"])
@login_required
def api_get_settings():
    settings = get_settings()
    is_superadmin = session.get("role") == "superadmin"
    return jsonify({"ok": True, "settings": public_settings(settings, is_superadmin)})


@app.route("/api/settings", methods=["PUT"])
@login_required
@superadmin_required
def api_update_settings():
    payload = request.get_json(force=True) or {}
    if not payload.get("confirmed"):
        return jsonify({"ok": False, "error": "Confirmation is required for setup changes."}), 400
    updates = payload.get("settings") or {}
    if not updates:
        return jsonify({"ok": False, "error": "No settings provided."}), 400
    try:
        saved = save_settings(updates)
        if "secret_key" in updates:
            app.secret_key = saved["secret_key"]
        return jsonify({"ok": True, "settings": public_settings(saved, True)})
    except ValueError as exc:
        return jsonify({"ok": False, "error": str(exc)}), 400


@app.route("/download")
def download_image():
    filename = request.args.get("filename")
    if not filename:
        abort(400, description="Filename is required.")
    file_path = os.path.join(TEMP_DIR, os.path.basename(filename))
    if not os.path.isfile(file_path):
        abort(404, description="File not found.")
    return send_file(file_path, as_attachment=True)


# Backward-compatible aliases used by older bookmarks / scheduled checks
@app.route("/send-now", methods=["GET", "POST"])
@login_required
def send_now():
    log = run_daily_tasks()
    return jsonify({"ok": True, "log": log})


@app.route("/selfcheck")
@login_required
def selfcheck():
    card_path = generate_birthday_card("RorYinBoT")
    response = test_whatsapp_connection(card_path)
    return jsonify({"ok": "Success" in str(response), "result": str(response)})


if __name__ == "__main__":
    app.run(debug=True)
