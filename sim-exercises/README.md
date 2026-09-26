# Simulation quizzes as interactive Jupyter notebooks

> **Note:** this README only covers the five `*Quiz_exercise` folders listed in the table below. The other folders of `sim-exercises/` (for example `SimplePowderDiffractometer`) are separate exercises and are not described here.

This folder contains the five simulation quizzes of the course as interactive Jupyter notebooks. They were converted with Claude (Anthropic) from the Moodle quizzes of the *Swedness 2024* course on the PaN e-learning platform (https://e-learning.pan-training.eu/mod/quiz/attempt.php?attempt=3343&cmid=3096):

| Folder | Moodle quiz |
|---|---|
| `ImagingQuiz_exercise` | Simulation quiz: Bragg Edge Imaging on Viking Sword (L10) |
| `PowderQuiz_exercise` | Simulation quiz: Diffraction from powder (L7) |
| `ReflectometerQuiz_exercise` | Simulation quiz: Reflectometer (L5) |
| `SANSQuiz_exercise` | Simulation quiz: Small Angle Neutron Scattering (L11) |
| `TripleAxisQuiz_exercise` | Simulation quiz: Ni single crystal in a Triple Axis Spectrometer (L13) |

## How to use the notebooks

Open the notebook and run **Run > Run All Cells**. The answer fields and the Check buttons only appear after the cells have been run. `ipywidgets` must be installed (it is part of most Jupyter installations).

Each folder contains:

- `<Quiz>_exercise.ipynb`: the quiz for the students.
- `<Quiz>_exercise_SOLUTIONS.ipynb`: the same quiz, with a *Solution* section after each question (correct answer and Moodle's general feedback). Not published on GitHub.
- `quiz_widgets.py`: the Python module that displays the answer fields and handles the Check buttons.
- `quiz_data.json`: the answer options, the correct answers and all the Moodle feedback of the quiz.
- the images used by the questions and by the feedback (`feedback_*.png`).

`quiz_widgets.py` and `quiz_data.json` must stay next to the notebook.

## What the notebooks reproduce from Moodle

- The text of the questions, with the same formatting (bold, lists, formulas) and the same images.
- The question types: single choice (round buttons), multiple choice (tick boxes), numerical answers and fill-in blanks, drop-down menus (matching, gap select, drag and drop into text), and drag and drop of markers onto an image.
- The *interactive with multiple tries* behaviour: the same number of tries as in Moodle for each question; after a wrong answer, the feedback, the hint of that try and a *Try again* button; when the question is finished (correct, or no tries left), Moodle's general feedback, including its images, and for the Reflectometer and Triple Axis quizzes the correct answer, as Moodle shows it.
- The feedback texts: the feedback of each answer option, the "Your answer is correct / partially correct / incorrect" messages, the hints of each try, the feedback of each field of the fill-in questions, and the general feedback.

## How the answers and feedback were collected

Moodle does not show the correct answers before a question is finished. To get them, the five quizzes were answered on a student account:

1. In a first attempt, each question was answered wrongly until the tries were used up, to collect the hints of every try and the feedback of the options. The attempt was then finished, and the review page gave the correct answers.
2. In a second attempt, each question was answered correctly, to collect the feedback given for a correct answer. For numerical answers, values 10 % and 2 % away from the correct value were tried first, to measure the tolerance Moodle accepts.

**Tolerances used for the numerical answers** (Bragg edge Q2, Q6, Q7, Q9; Powder Q1; Reflectometer Q3, Q6-Q11, Q14; Triple Axis Q3, Q6, Q7, Q9, Q12):

- Moodle accepted a value 10 % off: 10 % is used (it may accept more).
- Moodle accepted 2 % off but not 10 %: 2 % is used.
- Moodle only accepted the exact value (2 % was rejected): 1 % is used.
- Powder Question 1 (8000) has only one try in Moodle, so the tolerance could not be measured: 1 % is used.

**Grading of the multiple choice questions:** a question is correct when all the correct options are ticked. When Moodle also accepted all options ticked (wrong options not penalised), the notebook does the same. Otherwise, some correct options give *partially correct*.

**Missing feedback:**

- Bragg edge Question 1: the second hint could not be collected (the first try had already been used).
- When a feedback state was never seen in Moodle (for example the "incorrect" message of a question answered correctly at the first try), Moodle's standard text ("Your answer is incorrect.") is used.

## Drag and drop of markers

Moodle does not publish the drop zones of these questions, so the notebooks use zones reconstructed by Claude from the images and from Moodle's solution feedback:

- **Powder Q10 (Miller indices):** zones around the positions of the Ni peaks, calculated with Bragg's law for $\lambda_0 = 1$ Å (the default): (111) 28.6°, (200) 33.1°, (220) 47.4°, (311) 56.3°, (222) 59.0°. (100) and (120) are forbidden for an fcc lattice and must not be placed.
- **SANS Q1:** the six panels of the web page; the bottom row holds the log representations (as stated in Moodle's hint).
- **Triple Axis Q5:** the rows of the instrument interface (EI, EF, QHK for both qh and qk, QL, Temperature_K, neutron rays, simulation steps).
- **Bragg edge Q8 and Q11 (rust):** approximate zones. They were deduced from Moodle's solution images and from a McStas simulation of the sword. The drawing of the sword on which the markers are dropped is not to scale and it is not known which edge of the blade the detector image corresponds to, so these zones are generous: Q8 accepts the middle part of the blade; Q11 expects the two rust lines along the blade (±1.5 cm from its centre) and the rusty edge (either edge is accepted).

A marker is correct when its crosshair is inside a zone with the same label; markers placed on the image outside the right zone count as wrong.

## Files that are referred to in the quizzes

**Created by Claude (they were not available):**

- `ImagingQuiz_exercise/neutron_imaging_division.ipynb` (Question 10): reads the McStas images with and without the sword from `my_data/data.dat` and `my_data/background.dat`, and plots the transmission image data / background.
- `ImagingQuiz_exercise/neutron_imaging_Bragg_edge_division.ipynb` (Question 11): reads two radiograms taken on each side of the Bragg edge from `my_data/data_short.dat` and `my_data/data_long.dat`, and plots their ratio and its logarithm.
- `ImagingQuiz_exercise/example_data/`: example data used by these two notebooks when `my_data` does not exist. Simulated with McStas 3.8.5 (instrument `Radiography_Sword`), 1E7 neutron rays, pinhole_diameter=0.01 m, pinhole_detector_distance=25 m, pinhole_sample_distance=24.95 m (the settings given in Moodle's feedback):
  - `data_4.3A.dat` and `background_4.3A.dat`: chopper_mode=3, Lambda=4.3 Å, Sample=1 and Sample=0.
  - `bragg_edge_3.7A.dat` and `bragg_edge_4.3A.dat`: chopper_mode=2, Lambda=3.7 Å and 4.3 Å, Sample=1.

  The results agree with Moodle's solutions: the division removes the beam features (Question 10), and the Bragg edge ratio shows the two rust lines and the rusty edge (Question 11).

**Taken from the McStas examples** (`share/mcstas/resources/examples/elearning` of the McStas installation), in the `instrument/` folders:

- `ImagingQuiz_exercise/instrument/Sword_ODIN.instr` and `Filters.tgz`: the example `Radiography_Sword`, which has the same parameters as Sword_ODIN. The instrument was renamed and its output file renamed from `absoprtion_picture.dat` (typo in the original) to `absorption_picture.dat`, as written in the quiz. Used for the simulations of Questions 1, 3, 8, 10 and 11.
- `PowderQuiz_exercise/instrument/SimplePowderDiffractometer.instr`: same parameters as in the quiz. Used for the simulations of Questions 1-5 and 8-10.
- `SANSQuiz_exercise/instrument/SANSsimpleSpheres.instr`: the hard spheres version, with the parameters used in the quiz (R, dR, Lambda, DLambda...). Used for the simulations of Questions 1, 2, 6 and 7.

These should be the instruments installed on VISA, but this has not been checked.

**Not found:**

- `reflectometer_alignment.instr` (Reflectometer quiz). Needed from the second introduction text onwards, for the simulations of Questions 3, 4 and 8-14. The `Reflectometer` example of McStas has different parameters (no beamstop, no detector window), so it was not used.
- `Ni_TAS.instr` (Triple Axis quiz, also available as a web simulation at https://sim.e-neutrons.esss.dk/instrument/swedness/Ni_TAS). Needed for Question 5 (the interface) and for the simulations of Questions 6, 7 and 10-12. McStas has no triple axis instrument with a Ni single crystal.

## Issues found in the Moodle quizzes

- **Bragg edge Question 9:** the expected short wavelength is 3.7 Å, which is outside the range of chopper_mode 3 (3.8-8.8 Å), the answer to Question 7. Both radiograms need a chopper mode covering 3.7 Å and 4.3 Å, for example chopper_mode 2 (2.5-6.5 Å). This is written in `neutron_imaging_Bragg_edge_division.ipynb`.
- **Triple Axis Question 4:** the second option is displayed as just "$E_i$" in Moodle; the "<" of "$E_i < E_f$" is lost in the TeX. The notebook shows "$E_i < E_f$".
- Some typos of the Moodle texts were kept as they are (for example "agian", "perameters", "seperates peaks").

## Editing the answers

In `quiz_data.json`, the answer key and the feedback of each question are stored in the field `fb`, encoded in base64 so that the answers are not readable at a glance (a student can still decode them). To read or change them:

```python
import base64, json

data = json.load(open("quiz_data.json", encoding="utf-8"))
fb = json.loads(base64.b64decode(data["questions"]["3"]["fb"]))   # question 3
print(fb["key"], fb["tries"], fb["hints"])
# ... edit fb ...
data["questions"]["3"]["fb"] = base64.b64encode(json.dumps(fb, ensure_ascii=False).encode()).decode()
json.dump(data, open("quiz_data.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
```

`key` holds the indices of the correct options (counted from 0), or one entry per field for the fill-in questions: `{"value": ..., "tol": ...}` for numbers, the correct choice for drop-down menus.

## Status

The notebooks have not been imported into VISA yet.
