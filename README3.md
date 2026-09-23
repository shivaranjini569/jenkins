Yes. Let’s do **Question 6 from scratch**, exactly matching the task you were given.

The key idea is:

```text
Checkout
   ↓
Parallel Checks
   ├── frontend_check.py ──┐
   │                       │
   └── backend_check.py ───┤  run at the same time
                           ↓
                    Archive Reports
                           ↓
                  frontend_report.txt
                  backend_report.txt
```

Because your Jenkins setup has **2 executors**, the two checks can run simultaneously.

---

# Question 6 — What the examiner wants

You need to demonstrate **four things**:

1. Jenkins checks out your GitHub code.
2. `frontend_check.py` and `backend_check.py` run **in parallel**.
3. Each takes 4 seconds and creates its own report.
4. Jenkins archives both reports, and an **older build's archived reports remain available** after a newer build.

---

# PART 1 — Create the project

Create a new folder:

```text
Jenkins-Q6-Parallel
```

Inside it create:

```text
Jenkins-Q6-Parallel/
│
├── frontend_check.py
└── backend_check.py
```

---

# PART 2 — Create `frontend_check.py`

Put this in `frontend_check.py`:

```python
import time

print("Starting frontend check...")
time.sleep(4)

with open("frontend_report.txt", "w") as file:
    file.write("Frontend check completed successfully.\n")

print("Frontend check completed.")
```

### What it does

It:

```text
prints message
   ↓
waits 4 seconds
   ↓
creates frontend_report.txt
   ↓
writes result
```

---

# PART 3 — Create `backend_check.py`

Put this in `backend_check.py`:

```python
import time

print("Starting backend check...")
time.sleep(4)

with open("backend_report.txt", "w") as file:
    file.write("Backend check completed successfully.\n")

print("Backend check completed.")
```

It similarly:

```text
prints message
   ↓
waits 4 seconds
   ↓
creates backend_report.txt
   ↓
writes result
```

---

# PART 4 — Test both scripts locally

Before Jenkins, make sure the Python scripts work.

Run:

```cmd
python frontend_check.py
```

Wait about 4 seconds.

You should get:

```text
Starting frontend check...
Frontend check completed.
```

And:

```text
frontend_report.txt
```

should appear.

Now run:

```cmd
python backend_check.py
```

You should get:

```text
Starting backend check...
Backend check completed.
```

and:

```text
backend_report.txt
```

should appear.

---

# PART 5 — Check the report files

You should now have:

```text
Jenkins-Q6-Parallel/
│
├── frontend_check.py
├── backend_check.py
├── frontend_report.txt
└── backend_report.txt
```

For your GitHub repository, we actually don't need to commit the generated `.txt` files.

So delete:

```text
frontend_report.txt
backend_report.txt
```

before pushing.

We want Jenkins to create them during the build.

---

# PART 6 — Create GitHub repository

Create a new repository, for example:

```text
jenkins-q6-parallel
```

Put these files into it:

```text
frontend_check.py
backend_check.py
```

---

# PART 7 — Push to GitHub

Open the VS Code terminal inside your project.

Run:

```cmd
git init
```

Then:

```cmd
git add frontend_check.py backend_check.py
```

Then:

```cmd
git commit -m "Add parallel frontend and backend checks"
```

Then:

```cmd
git branch -M main
```

Then:

```cmd
git remote add origin YOUR_GITHUB_URL
```

Replace that with your actual GitHub repository URL.

Finally:

```cmd
git push -u origin main
```

Check GitHub.

You should see:

```text
frontend_check.py
backend_check.py
```

---

# PART 8 — Create Jenkins Pipeline

Open:

```text
http://localhost:8080
```

From Jenkins Dashboard:

### Click

**New Item**

### Name

```text
Q6-Parallel-Reports
```

### Select

**Pipeline**

Then click:

**OK**

---

# PART 9 — Go to Pipeline section

Scroll down to:

**Pipeline**

For:

**Definition**

select:

```text
Pipeline script
```

Then paste the following code.

---

# ⭐ FINAL PIPELINE SCRIPT

Replace the GitHub URL with your actual repository URL.

```groovy
pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/YOUR_USERNAME/jenkins-q6-parallel.git'
            }
        }

        stage('Parallel Checks') {
            parallel {

                stage('Frontend Check') {
                    steps {
                        bat 'python frontend_check.py'
                    }
                }

                stage('Backend Check') {
                    steps {
                        bat 'python backend_check.py'
                    }
                }
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'frontend_report.txt,backend_report.txt',
                                 fingerprint: true
            }
        }
    }
}
```

---

# PART 10 — Understand the Pipeline

Don't just memorize it. Understand each part.

---

## Stage 1 — Checkout

```groovy
stage('Checkout') {
    steps {
        git branch: 'main',
            url: 'YOUR_GITHUB_URL'
    }
}
```

This gets:

```text
frontend_check.py
backend_check.py
```

from GitHub into the Jenkins workspace.

---

# Stage 2 — Parallel Checks

This is the most important part.

```groovy
stage('Parallel Checks') {
    parallel {
```

Inside we have two stages:

```groovy
stage('Frontend Check')
```

and:

```groovy
stage('Backend Check')
```

So Jenkins can execute:

```text
          Parallel Checks
           /           \
          /             \
         ↓               ↓
Frontend Check     Backend Check
     ↓                   ↓
python frontend...  python backend...
     ↓                   ↓
   4 sec               4 sec
```

Because they run side by side, the total is approximately:

```text
4 seconds
```

plus a little Jenkins overhead.

---

# PART 3 — Frontend branch

```groovy
stage('Frontend Check') {
    steps {
        bat 'python frontend_check.py'
    }
}
```

Jenkins runs:

```cmd
python frontend_check.py
```

This waits:

```python
time.sleep(4)
```

then creates:

```text
frontend_report.txt
```

---

# PART 4 — Backend branch

```groovy
stage('Backend Check') {
    steps {
        bat 'python backend_check.py'
    }
}
```

Jenkins runs:

```cmd
python backend_check.py
```

It also waits 4 seconds and creates:

```text
backend_report.txt
```

---

# PART 5 — Archive Reports

After **both parallel branches finish**, Jenkins reaches:

```groovy
stage('Archive Reports')
```

and runs:

```groovy
archiveArtifacts artifacts: 'frontend_report.txt,backend_report.txt',
                 fingerprint: true
```

This tells Jenkins:

> Save these files as build artifacts.

So they are associated with that specific build.

---

# PART 11 — Save

Click:

**Save**

---

# PART 12 — Build #1

Click:

**Build Now**

Wait for the Pipeline to finish.

Open:

```text
Build #1
```

Then:

**Console Output**

---

# PART 13 — What you should see

You should see the Checkout stage first.

Then:

```text
Parallel Checks
```

And both scripts should execute.

You may see output resembling:

```text
Starting frontend check...
Starting backend check...
Frontend check completed.
Backend check completed.
```

The exact ordering of those lines can vary because they are running in parallel.

Then:

```text
Archive Reports
```

and finally:

```text
Finished: SUCCESS
```

---

# PART 14 — Check the timing

This is a part of your assessment question.

Each script contains:

```python
time.sleep(4)
```

### If run one after another

It would roughly take:

```text
Frontend = 4 sec
Backend  = 4 sec

Total ≈ 8 sec
```

plus startup/checkout/Jenkins overhead.

### In parallel

Both start around the same time:

```text
Frontend ───────── 4 sec
Backend  ───────── 4 sec
```

So:

```text
Parallel total ≈ 4 sec
```

plus overhead.

### What should you tell the examiner?

> Each individual check takes approximately 4 seconds. If they were executed sequentially, the two checks would take approximately 8 seconds. Because Jenkins executes them in parallel, the parallel stage should take roughly 4 seconds plus Jenkins overhead.

Don't claim that it will be **exactly** 4.00 seconds. Your machine, Jenkins startup, checkout, and process overhead will affect the actual time.

---

# PART 15 — Check the archived artifacts

After Build #1 succeeds, go to:

```text
Q6-Parallel-Reports
   ↓
Build #1
```

Look for:

### **Artifacts**

You should see:

```text
frontend_report.txt
backend_report.txt
```

Click each one.

You should see:

```text
Frontend check completed successfully.
```

and:

```text
Backend check completed successfully.
```

---

# PART 16 — Build #2

Now simply click:

**Build Now**

again.

Jenkins creates:

```text
Build #2
```

Wait until it finishes.

You should again get:

```text
frontend_report.txt
backend_report.txt
```

under Build #2.

---

# PART 17 — Prove old artifacts still exist

This is the final requirement.

Go back to:

```text
Q6-Parallel-Reports
```

Open:

```text
Build #1
```

You should **still** see:

```text
Artifacts

frontend_report.txt
backend_report.txt
```

Now open:

```text
Build #2
```

It also has:

```text
frontend_report.txt
backend_report.txt
```

---

# 🧠 What does that prove?

It proves that archived artifacts belong to their individual build records.

So:

```text
Build #1
├── frontend_report.txt
└── backend_report.txt

Build #2
├── frontend_report.txt
└── backend_report.txt
```

Running Build #2 does **not automatically overwrite the archived artifacts belonging to Build #1**.

Each build retains its archived artifact copies, subject to Jenkins build/artifact retention settings.

---

# 🔥 What you should say in the assessment

If the examiner asks:

### "Why use parallel?"

Say:

> Parallel execution allows the frontend and backend checks to run at the same time, reducing the total execution time compared with sequential execution.

### "How long should the parallel stage take?"

Say:

> Each script sleeps for 4 seconds, so the parallel stage should take approximately 4 seconds plus Jenkins overhead, whereas sequential execution would take approximately 8 seconds plus overhead.

### "What does `archiveArtifacts` do?"

Say:

> It stores the generated files as artifacts of the Jenkins build so they can be accessed from that build later.

### "Why are Build #1 artifacts still available after Build #2?"

Say:

> Jenkins archives artifacts per build. Build #2 creates its own archived copies, while Build #1's archived copies remain associated with Build #1 unless build/artifact retention removes them.

---

# 🧠 Memorize the Pipeline structure

When you see Q6 in the exam, think:

```text
pipeline
   ↓
agent any
   ↓
Checkout
   ↓
Parallel Checks
   ├── Frontend
   └── Backend
   ↓
Archive Reports
```

The most important syntax is:

```groovy
parallel {

    stage('Frontend Check') {
        steps {
            bat 'python frontend_check.py'
        }
    }

    stage('Backend Check') {
        steps {
            bat 'python backend_check.py'
        }
    }
}
```

And:

```groovy
archiveArtifacts artifacts: 'frontend_report.txt,backend_report.txt',
                 fingerprint: true
```

---

# ✅ Final files

### `frontend_check.py`

```python
import time

print("Starting frontend check...")
time.sleep(4)

with open("frontend_report.txt", "w") as file:
    file.write("Frontend check completed successfully.\n")

print("Frontend check completed.")
```

### `backend_check.py`

```python
import time

print("Starting backend check...")
time.sleep(4)

with open("backend_report.txt", "w") as file:
    file.write("Backend check completed successfully.\n")

print("Backend check completed.")
```

### Jenkins Pipeline

```groovy
pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/YOUR_USERNAME/jenkins-q6-parallel.git'
            }
        }

        stage('Parallel Checks') {
            parallel {

                stage('Frontend Check') {
                    steps {
                        bat 'python frontend_check.py'
                    }
                }

                stage('Backend Check') {
                    steps {
                        bat 'python backend_check.py'
                    }
                }
            }
        }

        stage('Archive Reports') {
            steps {
                archiveArtifacts artifacts: 'frontend_report.txt,backend_report.txt',
                                 fingerprint: true
            }
        }
    }
}
```

## ⚠️ One thing to check before the exam

Your Jenkins must have **at least 2 available executors** for genuine side-by-side execution. If there is only 1 executor, Jenkins cannot actually run both branches simultaneously on that node, and your timing demonstration won't show the intended parallel advantage.

For **your current Jenkins setup**, you already have 2 executors, so that's the setup you should use.

The three demonstrations you need to remember are:

```text
BUILD #1
   ↓
2 reports archived ✅

BUILD #2
   ↓
2 new reports archived ✅
   ↓
Build #1 reports still available ✅
```

and:

```text
Sequential ≈ 8 sec
Parallel   ≈ 4 sec
```

plus Jenkins overhead.
