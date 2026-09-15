# app/core/constants.py

RESERVED_USERNAMES = {
    # app routes
    "pin-creation-tool",
    "settings",
    "admin",
    "api",
    "auth",
    "users",
    "pins",
    "uploads",
    "boards",
    "login",
    "register",
    "logout",
    "about",
    "help",
    "support",
    "terms",
    "privacy",
    "static",
    "docs",
    "openapi.json",
    # generic reserved words worth blocking regardless of current routes
    "root",
    "null",
    "undefined",
    "www",
    "app",
}