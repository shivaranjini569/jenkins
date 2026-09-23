Yes. **For Question 3, use the following as your final lab answer.** It includes the Python script, GitHub steps, Jenkins steps, the complete Pipeline script, and exactly how to demonstrate **Release** and **Abort**.

> **Question 3:** Design a pipeline with the stages **Checkout, Build** (a compile check of `app.py` using `py_compile`), and **Deploy**. Define `APP_NAME` and `APP_VERSION` as custom variables in an `environment` block. The Deploy stage must pause with an input step that asks **"Approve deployment of `<APP_NAME>` version `<APP_VERSION>`?"** and has an OK button labelled **"Release"**. It should then run `app.py`. Demonstrate both outcomes, clicking Release in one build and Abort in another, and explain the result of each.

---

# 1. What you are building

Remember this picture:

```text
GitHub
   ↓
Checkout
   ↓
Build
   ↓
py_compile app.py
   ↓
Deploy
   ↓
┌─────────────────────────────────────────┐
│ Approve deployment of StudentPortal     │
│ version 1.0?                            │
│                                         │
│              [ Release ] [ Abort ]      │
└─────────────────────────────────────────┘
       ↓                    ↓
   Release                 Abort
       ↓                    ↓
 run app.py             deployment stops
       ↓
 SUCCESS
```

---

# 2. Create the Python program

Create a new project folder, for example:

```text
Jenkins-Q3-Deployment
```

Inside it create:

```text
app.py
```

Put this code in `app.py`:

```python
print("===================================")
print("APPLICATION DEPLOYED SUCCESSFULLY")
print("===================================")
print("Application: StudentPortal")
print("Version: 1.0")
print("Deployment completed.")
```

This is intentionally simple because **the main purpose of the question is the Jenkins Pipeline and manual approval**, not complicated Python logic.

---

# 3. Test `app.py` locally

Open the VS Code terminal in the project folder.

Run:

```cmd
python app.py
```

You should see:

```text
===================================
APPLICATION DEPLOYED SUCCESSFULLY
===================================
Application: StudentPortal
Version: 1.0
Deployment completed.
```

Now check syntax using the same command Jenkins will use:

```cmd
python -m py_compile app.py
```

If there is no output, that's normally a successful compile check.

---

# 4. Put the project on GitHub

Create a new GitHub repository, for example:

```text
jenkins-q3-deployment
```

Your repository should contain:

```text
jenkins-q3-deployment
└── app.py
```

From your VS Code terminal:

```cmd
git init
git add app.py
git commit -m "Add deployment application"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Replace:

```text
YOUR_GITHUB_REPOSITORY_URL
```

with your actual GitHub URL.

For example:

```cmd
git remote add origin https://github.com/username/jenkins-q3-deployment.git
```

Then check GitHub and make sure `app.py` is visible.

---

# 5. Create the Jenkins Pipeline

Open:

```text
http://localhost:8080
```

From the Jenkins Dashboard:

### Click

**New Item**

### Enter name

```text
Q3-Deployment-Pipeline
```

### Select

**Pipeline**

Then:

**OK**

---

# 6. Find the Pipeline section

Scroll down the configuration page until you find:

### Pipeline

For:

**Definition**

select:

```text
Pipeline script
```

You'll get a large script box.

---

# 7. Paste this COMPLETE Pipeline script

Replace the GitHub URL with your actual repository URL.

```groovy
pipeline {

    agent any

    environment {
        APP_NAME = 'StudentPortal'
        APP_VERSION = '1.0'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/YOUR_USERNAME/jenkins-q3-deployment.git'
            }
        }

        stage('Build') {
            steps {
                bat 'python -m py_compile app.py'
            }
        }

        stage('Deploy') {
            steps {

                input(
                    message: "Approve deployment of ${env.APP_NAME} version ${env.APP_VERSION}?",
                    ok: 'Release'
                )

                bat 'python app.py'
            }
        }
    }
}
```

---

# 8. Understand the script line by line

## `pipeline`

```groovy
pipeline {
```

This starts a Declarative Jenkins Pipeline.

---

## `agent any`

```groovy
agent any
```

Means Jenkins can execute the Pipeline on an available agent.

---

# 9. Environment block

This is specifically required by your question.

```groovy
environment {
    APP_NAME = 'StudentPortal'
    APP_VERSION = '1.0'
}
```

You have created two custom environment variables:

```text
APP_NAME     = StudentPortal
APP_VERSION  = 1.0
```

Inside the Pipeline we access them as:

```groovy
env.APP_NAME
env.APP_VERSION
```

---

# 10. Checkout stage

```groovy
stage('Checkout') {
    steps {
        git branch: 'main',
            url: 'YOUR_GITHUB_URL'
    }
}
```

This tells Jenkins:

> Go to GitHub, take the code from the `main` branch, and put it into the Jenkins workspace.

So:

```text
GitHub
   ↓
Jenkins workspace
   ↓
app.py
```

---

# 11. Build stage

The question specifically says:

> compile check of `app.py` using `py_compile`

So use:

```groovy
stage('Build') {
    steps {
        bat 'python -m py_compile app.py'
    }
}
```

This executes:

```cmd
python -m py_compile app.py
```

### What does it do?

It checks whether the Python file has valid syntax.

For example, this is valid:

```python
print("Hello")
```

But this has a syntax error:

```python
print("Hello"
```

If the compile check fails, Jenkins will not successfully reach the approval/deployment part.

---

# 12. Deploy stage

This is the most important part of Q3.

```groovy
stage('Deploy') {
```

Inside it:

```groovy
input(
    message: "Approve deployment of ${env.APP_NAME} version ${env.APP_VERSION}?",
    ok: 'Release'
)
```

Because:

```text
APP_NAME = StudentPortal
APP_VERSION = 1.0
```

Jenkins will display:

```text
Approve deployment of StudentPortal version 1.0?
```

And the approval button will be labelled:

```text
Release
```

The user can also choose:

```text
Abort
```

---

# 13. After approval

Immediately after the input step:

```groovy
bat 'python app.py'
```

So if you click **Release**, Jenkins runs:

```cmd
python app.py
```

and the application output appears in Console Output.

---

# 14. Save the Pipeline

Click:

**Save**

Now you're ready to run it.

---

# 15. BUILD 1 — Demonstrate RELEASE

On the Pipeline project page, click:

**Build Now**

Then open:

**Build #1 → Console Output**

The Pipeline will go through:

```text
Checkout
   ↓
Build
   ↓
Deploy
```

At Deploy, Jenkins will **pause**.

You'll see something like:

```text
Approve deployment of StudentPortal version 1.0?
```

with:

```text
Release
Abort
```

---

## Click `Release`

Click:

### **Release**

Now Jenkins continues to the next line:

```groovy
bat 'python app.py'
```

Your Console Output should contain:

```text
===================================
APPLICATION DEPLOYED SUCCESSFULLY
===================================
Application: StudentPortal
Version: 1.0
Deployment completed.
```

And the final result should be:

```text
Finished: SUCCESS
```

### What happened?

```text
Checkout       ✅
Build          ✅
Approval       ✅ Release
Run app.py     ✅
Pipeline       ✅ SUCCESS
```

---

# 16. BUILD 2 — Demonstrate ABORT

Now go back to the Pipeline project.

Click:

**Build Now**

This creates another build, for example:

```text
#2
```

Open:

**Build #2**

You'll again reach:

```text
Approve deployment of StudentPortal version 1.0?
```

This time click:

### **Abort**

---

# 17. What happens after Abort?

Jenkins stops the Pipeline at the `input` step.

This command:

```groovy
bat 'python app.py'
```

is **not executed**.

Therefore you should **not** see:

```text
APPLICATION DEPLOYED SUCCESSFULLY
```

The build will be shown as **ABORTED**.

Conceptually:

```text
Checkout       ✅
Build          ✅
Deploy         ✅ reached
Approval       ❌ Abort
Run app.py     ❌ NOT EXECUTED
Pipeline       ABORTED
```

---

# 18. This is exactly what you should explain to the examiner

### Release outcome

> When I click Release, the `input` step returns successfully, so the Pipeline continues to the `bat 'python app.py'` command. The application runs and the build completes successfully.

### Abort outcome

> When I click Abort, the input step is aborted, so the Pipeline stops at the approval stage. The `python app.py` command is not executed and the build is marked ABORTED.

---

# 19. Final Pipeline script — memorize this

This is the main answer you should have ready in the lab:

```groovy
pipeline {

    agent any

    environment {
        APP_NAME = 'StudentPortal'
        APP_VERSION = '1.0'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/YOUR_USERNAME/jenkins-q3-deployment.git'
            }
        }

        stage('Build') {
            steps {
                bat 'python -m py_compile app.py'
            }
        }

        stage('Deploy') {
            steps {

                input(
                    message: "Approve deployment of ${env.APP_NAME} version ${env.APP_VERSION}?",
                    ok: 'Release'
                )

                bat 'python app.py'
            }
        }
    }
}
```

Replace only this:

```text
https://github.com/YOUR_USERNAME/jenkins-q3-deployment.git
```

with your actual repository URL.

---

# 20. Your `app.py`

Keep this ready:

```python
print("===================================")
print("APPLICATION DEPLOYED SUCCESSFULLY")
print("===================================")
print("Application: StudentPortal")
print("Version: 1.0")
print("Deployment completed.")
```

---

# 🧠 Viva questions you are very likely to get

### Why do we use `py_compile`?

> It checks the syntax of the Python application before deployment without actually running the application.

### Why is `input` used?

> It provides a manual approval gate before deployment.

### Why `ok: 'Release'`?

> It changes the approval button label from the default to `Release`, as required.

### What happens when Release is clicked?

> The Pipeline continues and executes `app.py`.

### What happens when Abort is clicked?

> The Pipeline stops at the input step and `app.py` is not executed.

### What is `environment`?

> It defines environment variables that can be used by the Pipeline.

### Why use `${env.APP_NAME}`?

> It retrieves the `APP_NAME` environment variable defined in the Pipeline's `environment` block.

### What does `bat` mean?

> It executes a Windows batch command.

---

# 🔥 The 3 stages you should write from memory

When you see this question in your exam, think:

```text
CHECKOUT
   ↓
BUILD
   ↓
DEPLOY
```

Then:

```groovy
Checkout → git
Build    → python -m py_compile app.py
Deploy   → input → bat python app.py
```

That's the core of Q3.

### One very important exam detail

Don't click **Abort before the approval prompt appears**. For the required demonstration, let the Pipeline reach the Deploy approval screen, then make one build with **Release** and a separate build with **Abort**. That gives you the two outcomes the question explicitly asks you to demonstrate.
