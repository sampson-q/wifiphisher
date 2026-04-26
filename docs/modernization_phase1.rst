Phase 1 Modernization Foundations
=================================

This document describes the first incremental modernization step focused on safe
foundational improvements without rewriting stable wireless workflows.

What was introduced
-------------------

* ``wifiphisher/core/runtime_context.py``

  * Typed runtime session context for state that should not be module-global.
  * Tracks session ID, startup timestamp, parsed CLI args and discovered AP cache.

* ``wifiphisher/configuration/config.py``

  * Layered typed runtime configuration.
  * Supports defaults, environment overrides (``WIFIPHISHER_LOG_*``) and runtime overrides.
  * Adds strict validation for logging settings.

* ``wifiphisher/telemetry/logging.py``

  * Structured logging scaffolding with JSON formatter support.
  * Session correlation support through a log filter that injects ``session_id``.

Compatibility
-------------

The existing startup and attack flow remains unchanged.
The new modules are integrated as compatibility wrappers around current behavior:

* Logging still honors ``--logging`` and ``--logpath``.
* Existing handlers and file-based logging remain intact.
* Runtime context is introduced without removing operational capabilities.

Operational notes
-----------------

Optional environment overrides:

* ``WIFIPHISHER_LOG_LEVEL`` (CRITICAL|ERROR|WARNING|INFO|DEBUG|NOTSET)
* ``WIFIPHISHER_LOG_PATH`` (path to log file)
* ``WIFIPHISHER_LOG_JSON`` (true/false)

This phase is intended to enable subsequent modularization work
(event bus, plugin contracts, orchestration services) with lower risk.

