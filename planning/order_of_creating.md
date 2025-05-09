Thanks. Based on that structure, here's how you should prioritize and work through building the project step by step:

---

### 🔢 **Order of Script Development for `diamond-parser`**

#### 1. **`settings.json`**

* Define all paths, environment flags, version, and (eventually) logging config here.

#### 2. **`config/app_config.py`**

* Load and validate `settings.json`.
* Add a `get_config()` function to retrieve config values globally.

#### 3. **`main.py`**

* Minimal CLI entry point. Calls the pipeline runner with config path or default.
* Later you'll add argparse.

#### 4. **`pipeline/game_import_pipeline.py`**

* Rename to `parser_pipeline.py` or `play_parser.py` for clarity.
* This script controls the flow: load → parse → transform → export.

#### 5. **`core/file_manager.py`**

* Create `load_file()`, `save_file()` methods.
* Supports I/O from `data/raw`, `data/staging`, etc.

#### 6. **`parser/game_parser.py`**

* Reads loaded file contents, splits into lines/events.
* Later will call line-level parsing and transformer steps.

#### 7. **`core/transformer.py` (abstract base class)**

* Base logic for calling all other transformers.
* Interface used by `game_parser.py` or pipeline.

#### 8. **`core/transformers/` submodules**

* Build one at a time, starting with:

  * `team_transformer.py`: normalize team info
  * `player_transformer.py`: map player names/IDs
  * `event_transformer.py`: convert text events to structured tags
  * `line_filter_transformer.py`: skip irrelevant lines

#### 9. **`core/id_generator.py`**

* Generates unique game, team, player, play IDs (e.g., UUID or counter).

#### 10. **`core/normalizer.py`**

* Utility for normalizing player names, team names, etc.
* Called by transformers.

#### 11. **`parser/exporter.py` + `json_exporter.py` + `sqlite_exporter.py`**

* Pick one export format to support first (suggest JSON).
* Ensure the pipeline outputs structured data.

#### 12. **`core/version_manager.py`**

* Tracks settings file version or transformer versions.
* Optional; useful for debugging or upgrading configs.

---

### ✅ Suggested First Few Files to Start Writing

1. `settings.json`
2. `config/app_config.py`
3. `main.py`
4. `pipeline/game_import_pipeline.py` (rename!)
5. `core/file_manager.py`
6. `parser/game_parser.py`

---

Would you like me to generate starter templates for those first few scripts as a reference?
