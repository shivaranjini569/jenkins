Yes. This is **Question 4**, and it is very manageable once you separate it into three things:

```text
GitHub
   ↓
Checkout
   ↓
Show Build Info
   ↓
Run flake8
```

Then you will run it **twice**, compare the Jenkins variables, then deliberately add an unused import and run it again to produce the linter failure.

The question specifically requires the stages **Checkout, Show Build Info, and Run Linter**, and the linter must run on an `app.py` containing a `greet(name)` function.

---

# Question 4 — Complete Lab Procedure

## What you need at the end

You should be able to demonstrate:

### First build

```text
BUILD_NUMBER = 1
JOB_NAME = Q4-Linter-Pipeline
WORKSPACE = D:\...\workspace\Q4-Linter-Pipeline
```

and:

```text
flake8 app.py
Finished: SUCCESS
```

### Second build

```text
BUILD_NUMBER = 2
JOB_NAME = Q4-Linter-Pipeline
WORKSPACE = same workspace path
```

So:

| Value | Build 1 | Build 2 | What happens? |
|---|---|---|---|
| `BUILD_NUMBER` | 1 | 2 | **Changes** |
| `JOB_NAME` | Q4-Linter-Pipeline | Q4-Linter-Pipeline | **Stays same** |
| `WORKSPACE` | same job workspace | same job workspace | **Normally stays same** |

Then after adding an unused import:

```python
import os
```

Flake8 should report an unused-import error such as:

```text
F401 'os' imported but unused
```

and the build should fail.

---

# PART 1 — Create the Python project

Create a new folder in VS Code:

```text
Q4-Linter-Pipeline
```

Inside it create:

```text
app.py
```

So:

```text
Q4-Linter-Pipeline/
└── app.py
```

---

# PART 2 — Create `app.py`

For the **first successful version**, use:

```python
def greet(name):
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet("Jenkins"))
```

Save the file.

---

# PART 3 — Understand the code

The important requirement from the question is the function:

```python
def greet(name):
```

It takes one argument, `name`.

Then:

```python
return f"Hello, {name}!"
```

returns a greeting.

This part:

```python
if __name__ == "__main__":
```

makes the program execute the following when run directly:

```python
print(greet("Jenkins"))
```

So locally:

```cmd
python app.py
```

should print:

```text
Hello, Jenkins!
```

---

# PART 4 — Install Flake8

Before Jenkins can run:

```text
flake8 app.py
```

Flake8 needs to be installed on the machine where Jenkins is executing the build.

Open **Command Prompt** or your VS Code terminal:

```cmd
python -m pip install flake8
```

Then verify:

```cmd
flake8 --version
```

You should get a version number.

### If `flake8` is not recognized

Use:

```cmd
python -m flake8 --version
```

That tells us Python can find the package even when the `flake8` command itself isn't on PATH.

For the simplest lab setup, though, make sure this works:

```cmd
flake8 --version
```

because our Jenkins Pipeline will use `flake8 app.py`.

---

# PART 5 — Test Flake8 locally

Run:

```cmd
flake8 app.py
```

### What should happen?

For the correct code:

```python
def greet(name):
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet("Jenkins"))
```

Flake8 should produce **no output** and return successfully.

That's what we want.

Think:

```text
Correct Python
      ↓
flake8
      ↓
No lint errors
      ↓
SUCCESS
```

---

# PART 6 — Create GitHub repository

Create a new GitHub repository, for example:

```text
jenkins-q4-linter
```

Your repository should initially contain:

```text
jenkins-q4-linter/
└── app.py
```

---

# PART 7 — Push `app.py` to GitHub

In VS Code terminal:

```cmd
git init
```

Then:

```cmd
git add app.py
```

Then:

```cmd
git commit -m "Add greet application"
```

Then:

```cmd
git branch -M main
```

Then connect your GitHub repository:

```cmd
git remote add origin YOUR_GITHUB_REPOSITORY_URL
```

Replace that with your actual URL.

Finally:

```cmd
git push -u origin main
```

Go to GitHub and confirm that `app.py` is visible.

---

# PART 8 — Create the Jenkins Pipeline

Open:

```text
http://localhost:8080
```

From your Jenkins Dashboard:

### Click:

**New Item**

Enter:

```text
Q4-Linter-Pipeline
```

Select:

**Pipeline**

Click:

**OK**

---

# PART 9 — Find the Pipeline section

Scroll to the bottom of the configuration page.

Find:

### Pipeline

For:

**Definition**

select:

```text
Pipeline script
```

You'll get the large script box.

---

# PART 10 — Paste the Pipeline script

Replace the GitHub URL with yours.

```groovy
pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/YOUR_USERNAME/jenkins-q4-linter.git'
            }
        }

        stage('Show Build Info') {
            steps {
                bat 'echo BUILD_NUMBER=%BUILD_NUMBER%'
                bat 'echo JOB_NAME=%JOB_NAME%'
                bat 'echo WORKSPACE=%WORKSPACE%'
            }
        }

        stage('Run Linter') {
            steps {
                bat 'flake8 app.py'
            }
        }
    }
}
```

---

# PART 11 — Understand each stage

## Stage 1 — Checkout

```groovy
stage('Checkout') {
    steps {
        git branch: 'main',
            url: 'YOUR_GITHUB_URL'
    }
}
```

This gets `app.py` from GitHub into the Jenkins workspace.

Flow:

```text
GitHub
   ↓
Checkout
   ↓
Jenkins workspace
   ↓
app.py
```

---

# Stage 2 — Show Build Info

This is the special part of Question 4.

```groovy
stage('Show Build Info') {
    steps {
        bat 'echo BUILD_NUMBER=%BUILD_NUMBER%'
        bat 'echo JOB_NAME=%JOB_NAME%'
        bat 'echo WORKSPACE=%WORKSPACE%'
    }
}
```

These are Jenkins-provided environment variables.

### `BUILD_NUMBER`

The number of the current build.

First build:

```text
1
```

Second build:

```text
2
```

Third build:

```text
3
```

So this **changes every build**.

---

### `JOB_NAME`

The name of your Jenkins job.

You created:

```text
Q4-Linter-Pipeline
```

So it should remain:

```text
Q4-Linter-Pipeline
```

for every build of that same job.

Therefore:

> **JOB_NAME stays the same.**

---

### `WORKSPACE`

This is the folder in which Jenkins checks out your project and runs commands.

It will look something like:

```text
D:\JenkinsHome\workspace\Q4-Linter-Pipeline
```

For normal sequential builds of the same job, the workspace path generally stays the same.

Therefore, for your demonstration:

> **WORKSPACE should stay the same.**

---

# Stage 3 — Run Linter

```groovy
stage('Run Linter') {
    steps {
        bat 'flake8 app.py'
    }
}
```

Jenkins executes:

```cmd
flake8 app.py
```

If there are no lint errors:

```text
SUCCESS
```

If Flake8 finds an error:

```text
FAILURE
```

---

# PART 12 — Save

Click:

**Save**

---

# PART 13 — BUILD 1

Click:

**Build Now**

Wait for the build to complete.

Open:

```text
Build #1
```

Then:

**Console Output**

---

# PART 14 — What you should see in Build 1

Find the **Show Build Info** section.

You should see something similar to:

```text
BUILD_NUMBER=1
JOB_NAME=Q4-Linter-Pipeline
WORKSPACE=D:\JenkinsHome\workspace\Q4-Linter-Pipeline
```

Your exact workspace path may differ, so don't memorize the path.

Then:

```text
Run Linter
```

Flake8 should run.

Because the original `app.py` is clean, there should be no Flake8 error messages.

Finally:

```text
Finished: SUCCESS
```

---

# PART 15 — BUILD 2

Go back to:

```text
Q4-Linter-Pipeline
```

Click:

**Build Now**

Again.

Now open:

**Build #2 → Console Output**

Look at **Show Build Info**.

You should see something like:

```text
BUILD_NUMBER=2
JOB_NAME=Q4-Linter-Pipeline
WORKSPACE=D:\JenkinsHome\workspace\Q4-Linter-Pipeline
```

---

# PART 16 — Compare Build 1 and Build 2

Make this table during your assessment:

| Variable | Build #1 | Build #2 | Result |
|---|---|---|---|
| `BUILD_NUMBER` | 1 | 2 | **Changed** |
| `JOB_NAME` | Q4-Linter-Pipeline | Q4-Linter-Pipeline | **Same** |
| `WORKSPACE` | same path | same path | **Same** |

### What to tell the examiner

Say:

> `BUILD_NUMBER` changes because every new execution gets a new build number. `JOB_NAME` remains the same because both builds belong to the same Jenkins job. `WORKSPACE` normally remains the same because Jenkins is using the same job workspace for sequential builds.

---

# PART 17 — Now deliberately create a linter error

This is the second major part of Question 4.

Go back to `app.py`.

At the very top add:

```python
import os
```

So now your file becomes:

```python
import os


def greet(name):
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet("Jenkins"))
```

Save it.

---

# PART 18 — Understand why this should fail

We added:

```python
import os
```

but we never use `os`.

Flake8 checks for this and should report:

```text
F401 'os' imported but unused
```

`F401` means an imported module is not being used.

---

# PART 19 — Test locally first

Run:

```cmd
flake8 app.py
```

You should see an error similar to:

```text
app.py:1:1: F401 'os' imported but unused
```

That confirms that our deliberate mistake is working.

---

# PART 20 — Push the bad version to GitHub

Run:

```cmd
git add app.py
```

Then:

```cmd
git commit -m "Add unused import for linter test"
```

Then:

```cmd
git push
```

Now GitHub contains the intentionally faulty version.

---

# PART 21 — Run Jenkins again

Go to:

**Q4-Linter-Pipeline**

Click:

**Build Now**

This will create:

```text
Build #3
```

Open:

**#3 → Console Output**

---

# PART 22 — What should happen?

The stages should look like:

```text
Checkout
   ✅

Show Build Info
   ✅

Run Linter
   ❌
```

Flake8 should report something similar to:

```text
app.py:1:1: F401 'os' imported but unused
```

Then Jenkins should finish with a failed build, typically:

```text
Finished: FAILURE
```

---

# Why does the build fail?

Because this command:

```groovy
bat 'flake8 app.py'
```

returns a non-zero exit code when Flake8 finds an error.

Jenkins sees that the command failed and marks the stage/build as failed.

---

# 🧠 What to explain to your examiner

### First two builds

> The first two builds use the clean version of `app.py`, so Flake8 succeeds. `BUILD_NUMBER` changes from 1 to 2, while `JOB_NAME` remains the same and the workspace path remains the same for the same sequential job.

### Third build

> I added an unused `os` import. Flake8 detected it as `F401`, meaning the imported module is unused. Because the linter command returned an error, Jenkins marked the Run Linter stage and the build as failed.

---

# ⭐ Final Pipeline Script

This is the answer you should keep ready for the assessment:

```groovy
pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/YOUR_USERNAME/jenkins-q4-linter.git'
            }
        }

        stage('Show Build Info') {
            steps {
                bat 'echo BUILD_NUMBER=%BUILD_NUMBER%'
                bat 'echo JOB_NAME=%JOB_NAME%'
                bat 'echo WORKSPACE=%WORKSPACE%'
            }
        }

        stage('Run Linter') {
            steps {
                bat 'flake8 app.py'
            }
        }
    }
}
```

Replace:

```text
https://github.com/YOUR_USERNAME/jenkins-q4-linter.git
```

with your actual repository URL.

---

# ⭐ Final `app.py` — Successful Version

```python
def greet(name):
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet("Jenkins"))
```

---

# ⭐ `app.py` — Version Used to Demonstrate Failure

Add the unused import:

```python
import os


def greet(name):
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(greet("Jenkins"))
```

Then:

```text
flake8
   ↓
F401
   ↓
Run Linter FAILED
   ↓
Jenkins build FAILURE
```

---

# 🔥 Memorize this flow for Q4

When you see the question in the exam, think:

```text
New Item
   ↓
Pipeline
   ↓
Checkout
   ↓
Show Build Info
   ├── BUILD_NUMBER
   ├── JOB_NAME
   └── WORKSPACE
   ↓
Run Linter
   ↓
flake8 app.py
```

Then:

```text
Build #1 → SUCCESS
Build #2 → SUCCESS
Compare variables
       ↓
Add unused import
       ↓
Build #3
       ↓
F401 unused import
       ↓
FAILURE
```

**One thing to be careful about:** use the exact Jenkins job name you create when describing `JOB_NAME`, and use the actual workspace path shown by your Jenkins rather than memorizing an example path.
