Absolutely. Let’s do the **fresh Jenkins Pipeline task from scratch**, using `marks.py` instead of the old addition example.

I’ll give you the exact files, exact code, Jenkins clicks, and what you should expect at every stage.

# 🧪 Jenkins Pipeline Lab — Student Marks Calculator

## What you are going to build

The flow will be:

**VS Code → GitHub → Jenkins Pipeline → Checkout → Run Python → Display Result**

You will create:

```text
marks.py
```

Then Jenkins will run:

```text
python marks.py 80 75 90
```

and produce:

```text
=============================
STUDENT MARKS REPORT
=============================
Subject 1 : 80
Subject 2 : 75
Subject 3 : 90
Total     : 245
Average   : 81.67
=============================
```

---

# PART 1 — Create the Python program

## Step 1: Open VS Code

Open VS Code.

Create a new folder for this experiment.

For example:

```text
Jenkins-Marks-Pipeline
```

Open that folder in VS Code.

---

## Step 2: Create `marks.py`

Inside the folder, create:

```text
marks.py
```

Your structure should currently be:

```text
Jenkins-Marks-Pipeline/
└── marks.py
```

---

## Step 3: Paste this Python code

Put this inside `marks.py`:

```python
import sys

def calculate_marks(mark1, mark2, mark3):
    total = mark1 + mark2 + mark3
    average = total / 3
    return total, average


if __name__ == "__main__":

    mark1 = int(sys.argv[1])
    mark2 = int(sys.argv[2])
    mark3 = int(sys.argv[3])

    total, average = calculate_marks(mark1, mark2, mark3)

    print("=============================")
    print("STUDENT MARKS REPORT")
    print("=============================")
    print(f"Subject 1 : {mark1}")
    print(f"Subject 2 : {mark2}")
    print(f"Subject 3 : {mark3}")
    print(f"Total     : {total}")
    print(f"Average   : {average:.2f}")
    print("=============================")
```

---

# PART 2 — Understand the Python code

This is important for your lab viva.

### `import sys`

```python
import sys
```

Allows Python to receive values from the command line.

For example:

```text
python marks.py 80 75 90
```

The values `80`, `75`, and `90` are received through `sys.argv`.

---

### This function:

```python
def calculate_marks(mark1, mark2, mark3):
```

takes three marks.

Then:

```python
total = mark1 + mark2 + mark3
```

calculates the total.

And:

```python
average = total / 3
```

calculates the average.

---

### These lines:

```python
mark1 = int(sys.argv[1])
mark2 = int(sys.argv[2])
mark3 = int(sys.argv[3])
```

take the three values supplied from Jenkins.

For example:

```text
python marks.py 80 75 90
```

means:

```text
sys.argv[1] → 80
sys.argv[2] → 75
sys.argv[3] → 90
```

---

# PART 3 — Test Python BEFORE Jenkins

Do not immediately go to Jenkins.

First make sure the Python program works.

Open the VS Code terminal.

Run:

```bat
python marks.py 80 75 90
```

You should get approximately:

```text
=============================
STUDENT MARKS REPORT
=============================
Subject 1 : 80
Subject 2 : 75
Subject 3 : 90
Total     : 245
Average   : 81.67
=============================
```

### Try another example

```bat
python marks.py 60 70 80
```

Expected:

```text
Total     : 210
Average   : 70.00
```

If this works, your Python program is ready.

---

# PART 4 — Create GitHub Repository

Now we need Jenkins to obtain the Python file from GitHub.

Go to GitHub.

Create a **new repository**.

For example:

```text
jenkins-marks-pipeline
```

You can make it public for this lab.

Do not add unnecessary files.

---

# PART 5 — Push `marks.py` to GitHub

Go back to the VS Code terminal.

Make sure you are inside:

```text
Jenkins-Marks-Pipeline
```

Run:

```bat
git init
```

Then:

```bat
git add marks.py
```

Then:

```bat
git commit -m "Add marks calculator"
```

Rename the branch to main:

```bat
git branch -M main
```

Now connect your GitHub repository:

```bat
git remote add origin YOUR_GITHUB_REPOSITORY_URL
```

For example:

```bat
git remote add origin https://github.com/yourusername/jenkins-marks-pipeline.git
```

Then:

```bat
git push -u origin main
```

---

# PART 6 — Check GitHub

Open your GitHub repository.

You should see:

```text
jenkins-marks-pipeline

marks.py
```

Click `marks.py`.

Make sure your Python code is there.

**Only continue after you can see `marks.py` on GitHub.**

---

# PART 7 — Create Jenkins Pipeline

Now open Jenkins.

You already have Jenkins running at:

```text
http://localhost:8080
```

Your Jenkins setup is using:

```text
D:\JenkinsHome
```

so keep your Jenkins Command Prompt running.

---

## Step 1: Click New Item

On the Jenkins dashboard, click:

**New Item**

---

## Step 2: Enter project name

Enter:

```text
Jenkins-Marks-Pipeline
```

Select:

**Pipeline**

Then click:

**OK**

---

# PART 8 — Configure Pipeline

You will now see the configuration page.

Scroll down until you find:

## Pipeline

At the bottom, you should see:

```text
Definition
```

Choose:

```text
Pipeline script
```

Do **not** choose Pipeline script from SCM for this exercise.

---

# PART 9 — Paste the Jenkins Pipeline

Paste this:

```groovy
pipeline {

    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/YOUR_USERNAME/jenkins-marks-pipeline.git'
            }
        }

        stage('Calculate Marks') {
            steps {
                bat 'python marks.py 80 75 90'
            }
        }

        stage('Display Result') {
            steps {
                echo 'Student marks calculation completed successfully.'
            }
        }
    }
}
```

---

# ⚠️ VERY IMPORTANT

Change:

```groovy
https://github.com/YOUR_USERNAME/jenkins-marks-pipeline.git
```

to **your actual GitHub repository URL**.

For example:

```groovy
git branch: 'main',
    url: 'https://github.com/shivaranjini/jenkins-marks-pipeline.git'
```

Don't copy my example username.

Use your own repository URL.

---

# PART 10 — Understand the Pipeline

Your pipeline has three stages.

```text
Pipeline
│
├── Checkout Code
│
├── Calculate Marks
│
└── Display Result
```

---

## Stage 1 — Checkout Code

```groovy
stage('Checkout Code') {
    steps {
        git branch: 'main',
            url: 'YOUR_GITHUB_URL'
    }
}
```

This tells Jenkins:

> Go to GitHub and download the code from the `main` branch.

So Jenkins gets:

```text
marks.py
```

into the Jenkins workspace.

---

# Stage 2 — Calculate Marks

```groovy
stage('Calculate Marks') {
    steps {
        bat 'python marks.py 80 75 90'
    }
}
```

This is where Jenkins executes Python.

The command is:

```bat
python marks.py 80 75 90
```

Jenkins passes:

```text
80 → Subject 1
75 → Subject 2
90 → Subject 3
```

The Python program calculates:

```text
80 + 75 + 90 = 245
```

and:

```text
245 / 3 = 81.67
```

---

# Stage 3 — Display Result

```groovy
stage('Display Result') {
    steps {
        echo 'Student marks calculation completed successfully.'
    }
}
```

This simply prints a message in Jenkins.

---

# PART 11 — Why `bat`?

Because your Jenkins agent is running on **Windows**.

Therefore:

```groovy
bat 'python marks.py 80 75 90'
```

is used.

For Linux Jenkins agents, you commonly use:

```groovy
sh 'python marks.py 80 75 90'
```

### Remember this for your exam:

| Operating System | Jenkins command |
| ---------------- | --------------- |
| Windows          | `bat`           |
| Linux/macOS      | `sh`            |

---

# PART 12 — Save the Pipeline

After pasting the Pipeline:

Scroll down.

Click:

**Save**

You should now be taken to the Jenkins project page.

---

# PART 13 — Run the Pipeline

Click:

**Build Now**

You should see something like:

```text
Build History

#1
```

Click:

```text
#1
```

Then click:

**Console Output**

---

# PART 14 — What Jenkins should do

The console will contain lots of Jenkins information.

Look for the important parts.

First:

```text
Checkout Code
```

Jenkins should clone your GitHub repository.

Then:

```text
Calculate Marks
```

It should execute:

```text
python marks.py 80 75 90
```

You should see:

```text
=============================
STUDENT MARKS REPORT
=============================
Subject 1 : 80
Subject 2 : 75
Subject 3 : 90
Total     : 245
Average   : 81.67
=============================
```

Then:

```text
Student marks calculation completed successfully.
```

Finally:

```text
Finished: SUCCESS
```

🎉 That means your Pipeline worked.

---

# PART 15 — Your complete project structure

Your GitHub repository should contain:

```text
jenkins-marks-pipeline/
│
└── marks.py
```

Your Jenkins Pipeline contains:

```text
pipeline
│
├── agent any
│
├── Checkout Code
│   └── git
│
├── Calculate Marks
│   └── bat python marks.py
│
└── Display Result
    └── echo
```

---

# ⭐ PART 16 — Make it more like an actual exam

Once the first build works, don't stop.

Change the marks in the Pipeline:

```groovy
bat 'python marks.py 80 75 90'
```

to:

```groovy
bat 'python marks.py 95 88 76'
```

Save → **Build Now**.

Expected:

```text
Subject 1 : 95
Subject 2 : 88
Subject 3 : 76
Total     : 259
Average   : 86.33
```

This proves that you understand how the Jenkins Pipeline passes arguments to the Python program.

---

# 🧠 PART 17 — What to remember for your assessment

If the examiner asks:

### "What is `agent any`?"

Say:

> `agent any` tells Jenkins that the Pipeline can execute on any available Jenkins agent.

### "What does the Git step do?"

> It checks out the source code from the specified Git repository and branch.

### "Why did you use `bat`?"

> The Jenkins agent is running Windows, so `bat` is used to execute Windows command-line commands.

### "Why use `sys.argv`?"

> It allows the Python program to receive command-line arguments from Jenkins.

### "What happens during Checkout Code?"

```text
GitHub
   ↓
Jenkins
   ↓
Workspace
   ↓
marks.py
```

### "What happens during Calculate Marks?"

```text
Jenkins
   ↓
python marks.py 80 75 90
   ↓
Python receives arguments
   ↓
Calculates total
   ↓
Calculates average
   ↓
Prints result
```

### "What does `Finished: SUCCESS` mean?"

> All Pipeline stages completed successfully without an error.

---

# 🔥 Final code to keep for your lab

### `marks.py`

```python
import sys

def calculate_marks(mark1, mark2, mark3):
    total = mark1 + mark2 + mark3
    average = total / 3
    return total, average


if __name__ == "__main__":

    mark1 = int(sys.argv[1])
    mark2 = int(sys.argv[2])
    mark3 = int(sys.argv[3])

    total, average = calculate_marks(mark1, mark2, mark3)

    print("=============================")
    print("STUDENT MARKS REPORT")
    print("=============================")
    print(f"Subject 1 : {mark1}")
    print(f"Subject 2 : {mark2}")
    print(f"Subject 3 : {mark3}")
    print(f"Total     : {total}")
    print(f"Average   : {average:.2f}")
    print("=============================")
```

### `Jenkinsfile / Pipeline script`

```groovy
pipeline {

    agent any

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'YOUR_GITHUB_REPOSITORY_URL'
            }
        }

        stage('Calculate Marks') {
            steps {
                bat 'python marks.py 80 75 90'
            }
        }

        stage('Display Result') {
            steps {
                echo 'Student marks calculation completed successfully.'
            }
        }
    }
}
```

**Do this in order:** Python → test locally → GitHub → Jenkins Pipeline → Save → Build Now → Console Output → verify `SUCCESS`.

If you want to practice for the assessment, after this works I can give you a **second completely new Pipeline question without giving you the code**, and you can try writing the Python + Jenkinsfile yourself.
