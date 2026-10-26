# 🧩 Group Exercise — Building a Python Package for SEM Metadata with Git

---

## 1. Context and motivation

Scanning Electron Microscopes (SEMs) save each image as a TIFF file. Next to the pixels, the instrument writes a large block of **instrument metadata**: working distance, beam current, pixel size, detector, vacuum, stage position, and many more parameters. These values are essential for reproducibility and for making microscopy data **FAIR** (Findable, Accessible, Interoperable, Reusable), yet they are hidden inside the file and are rarely extracted systematically.

TIFF files store metadata as numbered **tags**. ZEISS SEMs write their instrument parameters as one long text block in the private tag **34118**. In this exercise you will work in a **group of three students** to finish a small Python package, `semmeta`, that:

1. walks through a nested folder of SEM images,
2. extracts the instrument metadata from tag 34118,
3. saves it as JSON,
4. cleans the values (e.g. `"WD = 3.18 mm"` → `"3.18 mm"`),
5. visualises each image together with a table of selected parameters,
6. is covered by automated tests.

Each student is responsible for **one module** and works on **their own Git branch**. At the end, the group merges the three branches into a complete, working pipeline.

## 2. Learning objectives

By the end of this exercise you should be able to:

- explain how a folder becomes a Python **package** (`__init__.py`, imports, `__all__`);
- read and parse binary-file metadata (TIFF tags) with **Pillow**;
- use **regular expressions** to separate numerical values from units;
- write clean, documented classes that follow a given **interface specification**;
- produce figures with **matplotlib** non-interactively;
- run **unit tests** with **pytest** and interpret their results;
- collaborate on a shared code base with **Git branches, pull requests and code review**.

---

## 3. Group setup

### 3.1 Roles

| Student | Branch | Module | Task |
|---|---|---|---|
| Student A | `metadata_extractor_module` | `semmeta/metadata_extractor_module.py` | Task 1 |
| Student B | `json_cleaner_module` | `semmeta/json_cleaner_module.py` | Task 2 |
| Student C | `visualizer_module` | `semmeta/visualizer_module.py` | Task 3 |

> ⚠️ **Rule:** each student modifies **only their own module**. Because the three files are independent, the final merges will not produce conflicts. If you think another file needs a change, discuss it with the group first.

### 3.2 Create the group repository (one student)

1. On GitHub, create a new **empty** repository for your group (do *not* add a
   README, .gitignore, or license). The name must follow this format:

       Py4DM1-name-of-the-group

2. Update your local copy of the course repository so you have the latest
   version of the exercise:

       cd python-2026
       git pull

3. Copy the exercise folder **outside** the course repository and turn it into
   a new Git repository:

       cd ..
       cp -r python-2026/<exercise-folder> Py4DM1-name-of-the-group
       cd Py4DM1-name-of-the-group
       git init -b main
       git add .
       git commit -m "Initial commit: exercise starter files"

4. Connect it to your group repository on GitHub and push:

       git remote add origin https://github.com/<user>/Py4DM1-name-of-the-group.git
       git push -u origin main

5. On GitHub, open **Settings → Collaborators** and add the other two students.
   They can then clone the group repository:

       git clone https://github.com/<user>/Py4DM1-name-of-the-group.git

> Do not run any of these commands inside the `python-2026` folder: your
> personal course copy should stay linked to the course repository so you can
> keep pulling updates.

### 3.3 Create your branch (every student)

```bash
git clone https://github.com/<user>/data-infra-name-of-the-group.git
cd data-infra-name-of-the-group
git checkout -b <your-branch-name>          # e.g. json_cleaner_module
```

Commit often, with meaningful messages, and push your branch:

```bash
git add semmeta/<your_module>.py
git commit -m "Implement clean_value with regex"
git push -u origin <your-branch-name>
```

> 💡 The `.gitignore` file already excludes `output/`, `__pycache__/` and `.pytest_cache/`. Never commit generated files.

---

## 4. Project structure

```
.
├── .gitignore                          # PROVIDED
├── imgs/                               # input data (nested on purpose!)
│   ├── 1/12_50_vero_09.tif
│   ├── 2/testdef/LIL test_defect02.tif # note: a space in the file name
│   ├── 3/protesi_anca1_08.tif
│   └── 4/perovskite-inside-010.tif
├── main.py                             # PROVIDED – runs the whole pipeline
├── requirements.txt                    # PROVIDED – Python dependencies
├── semmeta/
│   ├── __init__.py                     # PROVIDED – do not modify
│   ├── metadata_extractor_module.py    # Student A – 3 methods to implement
│   ├── json_cleaner_module.py          # Student B – __init__ given, 5 methods to implement
│   └── visualizer_module.py            # Student C – __init__ given, 4 methods to implement
└── tests/
    ├── conftest.py                     # PROVIDED
    └── test_semmeta.py                 # PROVIDED
```

Every method you must implement is already present as a **stub**: it has the correct name, arguments and a docstring, and its body is

```python
# TODO (Task N): implement this method
raise NotImplementedError("... is not implemented yet")
```

Replace these two lines with your implementation. **Do not rename methods or change their arguments**: `main.py`, `__init__.py` and the provided tests call your code by name.

Thanks to the stubs, `import semmeta` works from the start, so each student can test their own module without waiting for the others.

---

## 5. Environment setup (every student)

```bash
# 1. Create and activate a virtual environment (or use conda)
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 2. Install the dependencies — choose ONE of the two options
pip install -r requirements.txt          # option A: from the requirements file
pip install pillow matplotlib pytest     # option B: direct installation

# 3. Check that Python finds the images
python -c "from pathlib import Path; print(sorted(Path('imgs').rglob('*.tif')))"
```

Always run commands from the **project root** (the folder that contains `main.py`).

---

## 6. Task 0 — Explore before you code (every student, ≈ 20 min)

Before writing any code, get to know the data. In a Python shell:

```python
from PIL import Image
img = Image.open("imgs/1/12_50_vero_09.tif")
print(img.size, img.mode)
print(list(img.tag.keys()))          # which TIFF tags exist?
raw = img.tag[34118][0]               # the ZEISS instrument block
lines = raw.split("\r\n")
print(len(lines))
for i, line in enumerate(lines[:60]):
    print(i, repr(line))
```

Answer these questions together before moving on:

1. How many lines does the tag 34118 block contain?
2. What do the first lines look like?
3. Try the same with `imgs/3/protesi_anca1_08.tif` and `imgs/4/perovskite-inside-010.tif`. What is different?

---

## 7. Task 1 — Metadata extractor (Student A, ≈ 45 min)

**Branch:** `metadata_extractor_module` · **File:** `semmeta/metadata_extractor_module.py`

Read the existing class carefully: `ImageMetadata`, `GetInsMetadata` (a *property*), `InsMetaDict` and `ExtractMetadata`. Notice that `ExtractMetadata` calls `OpenCheckImage` first. Then implement the three stub methods.

### 7.1 `OpenCheckImage(self, image)`

| | |
|---|---|
| **Parameters** | `image` – path of the image file (`str`) |
| **Behaviour** | If the file name ends with one of the extensions in `self.semext`, try to open it with `PIL.Image.open`. If opening fails, print `"[ERROR]"` followed by the path. |
| **Returns** | The PIL `Image` object if the file was opened; `False` otherwise (wrong extension, missing file, unreadable file). |

> 💡 **Hints**
> - `str.endswith` accepts a **tuple** of suffixes: `"a.tif".endswith((".tif", ".tiff"))`.
> - A missing file and a corrupted file both raise exceptions that are subclasses of `OSError` (`IOError` is an alias). Use `try` / `except`.
> - One of the four images is corrupted on purpose. Your method must **not crash** on it.

### 7.2 `WriteSEMJson(self, file, semdict)`

| | |
|---|---|
| **Parameters** | `file` – output path (`str` or `pathlib.Path`); `semdict` – metadata dictionary |
| **Behaviour** | Serialises `semdict` to `file` as JSON with an indentation of 2 spaces. |
| **Returns** | `None` |

### 7.3 `WriteProcessingReport(self, file, records)`

| | |
|---|---|
| **Parameters** | `file` – output path; `records` – list of dictionaries, each with the keys `"image"` (path) and `"status"` (`"OK"` or `"ERROR"`, produced by `main.py`) |
| **Behaviour** | Writes a plain-text report with a title, a separator line of 60 `=`, an empty line, a header row, a separator line of 60 `-`, and one aligned row per record. |
| **Returns** | `None` |

Expected layout (status column 10 characters wide, left-aligned):

```
SEM IMAGE PROCESSING REPORT
============================================================

STATUS     IMAGE
------------------------------------------------------------
OK         imgs/1/12_50_vero_09.tif
OK         imgs/2/testdef/LIL test_defect02.tif
```

> 💡 **Hint:** f-strings support alignment: `f"{text:<10}"` pads `text` to 10 characters.

### Check your implementation

```python
from semmeta import SEMMeta

print(SEMMeta.OpenCheckImage("imgs/1/12_50_vero_09.tif"))          # expected: a PIL TiffImageFile object
print(SEMMeta.OpenCheckImage("imgs/4/perovskite-inside-010.tif"))  # expected: [ERROR] ... then False
print(SEMMeta.OpenCheckImage("notes.txt"))                         # expected: False
print(SEMMeta.OpenCheckImage("missing.tif"))                       # expected: [ERROR] ... then False

meta = SEMMeta.ExtractMetadata("imgs/1/12_50_vero_09.tif")
SEMMeta.WriteSEMJson("check_raw.json", meta)                       # open the file and look at it
SEMMeta.WriteProcessingReport("check_report.txt",
    [{"image": "imgs/1/12_50_vero_09.tif", "status": "OK"},
     {"image": "imgs/4/perovskite-inside-010.tif", "status": "ERROR"}])
```

Delete `check_raw.json` and `check_report.txt` afterwards (do not commit them). Then run `pytest -v -k "instrument or non_existing"` — these three tests should pass.

---

## 8. Task 2 — JSON cleaner (Student B, ≈ 60 min)

**Branch:** `json_cleaner_module` · **File:** `semmeta/json_cleaner_module.py`

The raw values extracted from the instrument look like `"WD = 3.18 mm"` or `"Beam Current = 13 pA"`. The cleaner keeps only the **number and its unit**.

The `__init__` method is **given**. Read it: why does it use `cleaned_data=None` instead of `cleaned_data={}`? (Hint: try `def f(x=[]): x.append(1); return x` and call `f()` three times.)

### Specification

| Method | Input | Output / behaviour |
|---|---|---|
| `__init__(cleaned_data=None)` | optional initial dictionary | **Given.** Stores it in `self.cleaned_data` (an empty `dict` if nothing is given). |
| `load_json(jsfile)` | path to a JSON file | Returns the file content as a Python `dict`. |
| `clean_value(value)` | a string |  **Given.** If the string contains a number followed by a unit, returns `"<number> <unit>"` (one space). Otherwise returns `value` **unchanged**. |
| `clean_dict(data)` | a `dict` | Returns a **new** `dict`: string values are cleaned with `clean_value`, entries whose value is `None` are **removed**, any other value is kept as it is. |
| `process(jsfile)` | path to a raw JSON file | Loads, cleans, stores the result in `self.cleaned_data` and **returns** it. |
| `save_cleaned(output_path)` | output path | Writes `self.cleaned_data` as JSON (indent = 2). |

### Check your implementation

```python
from semmeta import JsonCleaner

cleaner = JsonCleaner()

print(cleaner.clean_value("AP_WD = 3.18 mm"))         # expected: 3.18 mm
print(cleaner.clean_value("Beam Current = 13 pA"))    # expected: 13 pA
print(cleaner.clean_value("Detector = InLens"))       # expected: Detector = InLens  (no number + unit → unchanged)
print(cleaner.clean_value("Conjugate posn. = -164.00 mm"))  # expected: -164.00 mm  (keep the sign!)
print(cleaner.clean_value("Opt.Aperture = 2"))        # expected: Opt.Aperture = 2  (no unit → unchanged)

print(cleaner.clean_dict({"AP_WD": "WD = 3.18 mm", "AP_X": None, "AP_N": 5}))
# expected: {'AP_WD': '3.18 mm', 'AP_N': 5}
```

Then run `pytest -v -k clean` — the two cleaner tests should pass.

> 💡 **Hints**
> - `re.search(pattern, text)` returns a match object or `None`; `match.group(1)` gives the first captured group.
> - A first pattern to try: one group for digits and dots, optional whitespace, one group for letters.
> - Your branch does not contain Student A's code, so you cannot produce a `_raw.json` with `main.py` yet. Create a small one by hand, or extract one directly with `SEMMeta.ExtractMetadata(...)` + `json.dump`, and test your regex on real values: does `"Opt.Aperture = 2"` or `"C3 Rot Corrn. = On"` stay unchanged? Is the minus sign of `-164.00 mm` kept? Working only on the text after `=` helps a lot.

---

## 9. Task 3 — Visualizer (Student C, ≈ 60 min)

**Branch:** `visualizer_module` · **File:** `semmeta/visualizer_module.py`

The visualiser displays an SEM image (top) and a table of selected metadata (bottom) and saves the figure as a PNG.

The `__init__` method is **given**: it stores both paths, sets `self.metadata = {}` and defines `self.variables`, the six parameters to display.

### Specification

| Method | Behaviour |
|---|---|
| `__init__(json_path, image_path)` | **Given.** |
| `load_metadata()` | Reads the **cleaned** JSON file into `self.metadata`. |
| `clean_value(raw_value, variable_name=None)` | **Given.** Returns a **tuple of two strings** `(value, unit)`, e.g. `"3.18 mm"` → `("3.18", "mm")`. If `raw_value` is not a string, or no number + unit is found, returns `("N/A", "N/A")`. |
| `extract_variables()` | For every name in `self.variables` returns a tuple `(name, value, unit)`; missing variables give `(name, "N/A", "N/A")`. Returns a **list** of 6 tuples. |
| `show_image_with_table()` | Loads the metadata, builds a figure with two vertically stacked panels (grayscale image + table with the column labels `Variable`, `Value`, `Unit`), creates the folder `./output` if needed, saves the figure as `./output/<image name without extension>.png`, displays it, then closes it. |

### Check your implementation

Your branch does not contain the cleaner yet, so create a small test file by hand, `check_cleaned.json`:

```json
{
  "AP_WD": "3.198 mm",
  "AP_BEAM_TIME": "4669.97 Hours",
  "AP_IMAGE_PIXEL_SIZE": "25.09 nm",
  "AP_BEAM_CURRENT": "80.0 µA",
  "DP_DETECTOR": "InLens"
}
```

```python
from semmeta import SEMVisualizer

vis = SEMVisualizer("check_cleaned.json", "imgs/1/12_50_vero_09.tif")
vis.load_metadata()
print(vis.clean_value("3.18 mm"))     # expected: ('3.18', 'mm')
print(vis.clean_value(None))          # expected: ('N/A', 'N/A')
print(vis.extract_variables())
# expected: AP_WD, AP_BEAM_TIME, AP_IMAGE_PIXEL_SIZE, AP_BEAM_CURRENT with value and unit;
#           AP_HOLDER_HEIGHT and AP_HOLDER_DIAMETER with ('N/A', 'N/A')
vis.show_image_with_table()           # a window opens; output/12_50_vero_09.png is created
```

Delete `check_cleaned.json` afterwards (do not commit it).

> 💡 **Hints**
> - `fig, (ax_img, ax_table) = plt.subplots(2, 1, figsize=(8, 8))`
> - `ax_table.table(cellText=rows, colLabels=[...], loc="center")`, then `ax_table.axis("off")`
> - `os.path.splitext(os.path.basename(path))[0]` or `pathlib.Path(path).stem` gives the name without extension.
> - `os.makedirs("./output", exist_ok=True)`
> - Close your figures (`plt.close(fig)`) — `main.py` processes several images in a loop and open figures accumulate in memory.

---

## 10. Final task — Integration (whole group, ≈ 30 min)

### 10.1 Pull requests and code review

1. When your module works, push your branch and open a **Pull Request** into `main` on GitHub.
2. **Each pull request must be reviewed by another member of the group** before merging. The reviewer reads the code, runs the check script of section 7, 8 or 9 on the branch, and leaves at least one comment.
3. Merge the three pull requests one at a time. After each merge, the other students update their branch:

   ```bash
   git checkout main
   git pull
   ```

### 10.2 Run the provided tests

On the merged `main` branch:

```bash
pytest -v
```

The provided suite contains **6 tests**:

| Test | What it checks | Passes after |
|---|---|---|
| `test_instrument_metadata_dictionary` | list → dict conversion of instrument metadata | from the start (given code) |
| `test_empty_instrument_metadata` | empty input gives an empty dict | from the start (given code) |
| `test_clean_value` | `JsonCleaner.clean_value` extracts number + unit | Task 2 |
| `test_clean_dictionary` | `None` values are removed | Task 2 |
| `test_non_existing_image` | a missing file does not crash the pipeline | Task 1 |
| `test_processing_pipeline` | extract → `WriteSEMJson` → clean → save on a real image | Tasks 1 **and** 2 (only after merging) |

A test that calls an unfinished method fails with `NotImplementedError` — read the message, it tells you which method is missing.

**Goal:** all 6 tests pass on `main`.

### 10.3 Run the full pipeline

`main.py` takes the **root folder of the images** as argument and searches it recursively:

```bash
python main.py imgs
```

A figure window opens for each image; close it to continue with the next one. When the run is finished, the `output/` folder should contain:

```
output/
├── <image_name>_raw.json        # raw metadata, one per image
├── <image_name>_cleaned.json    # cleaned metadata, one per image
├── <image_name>.png             # image + metadata table, one per image
└── processing_report.txt        # OK / ERROR status of every image
```

Check that all four images appear in `processing_report.txt`. Open at least two figures and verify that the values in the table match the cleaned JSON.

---

## 🔄 Collaboration rules (summary)

- Each student works independently on their branch and modifies only their own module.
- Commit small steps with clear messages; push regularly.
- Open a **Pull Request** to merge your branch into `main`; it must be reviewed by a group member.
- The final `main` branch must contain a **complete, working pipeline** with all tests passing.

Good luck - and read the error messages: they almost always tell you exactly what is wrong.
