# Github Notes
https://github.com/AScotty27/Speedy7.git


`git log --reverse --pretty=oneline`
`q`
`git reset --hard 4600aef589e883e65992fa2573f61b6448fd1440`


### Steps to Contribute to a Git Repository

1. **Fork the Repository**
   - Go to the repository on GitHub.
   - Click "Fork" to create a copy under your account.

2. **Clone the Forked Repository**
   - `git clone https://github.com/simpledimplejohn/Speedy7.git`

3. **Add Original Repository as Remote**
   - `cd repository-name`
   - `git remote add upstream https://github.com/AScotty27/Speedy7.git`

4. **Create a New Branch**
   - `git checkout -b jbdev`

5. **Make Changes and Commit**
   - Make your changes.
   - `git add .`
   - `git commit -m "Description of changes"`

6. **Push Changes to Your Fork**
   - `git push origin jbdev`

7. **Create a Pull Request**
   - Go to your forked repository on GitHub.
   - Click "Compare & pull request".
   - Provide a title and description.
   - Click "Create pull request".

8. **Sync with Upstream Repository (Optional)**
   - `git fetch upstream`
   - `git checkout main`
   - `git merge upstream/main`
   - `git push origin main`
   - Update feature branch: `git checkout jbdev` and `git merge main`

This list provides a concise guide to cloning a Git repository, making changes, and creating a pull request.

### How to Push Changes to Your Fork

1. **Clone Your Fork**
   ```bash
   git clone https://github.com/your-username/repository-name.git
   ```

2. **Add the Original Repository as a Remote**
   ```bash
   cd repository-name
   git remote add upstream https://github.com/original-owner/repository-name.git
   ```

3. **Verify Remote URLs**
   ```bash
   git remote -v
   ```
   Ensure you see:
   ```
   origin    https://github.com/your-username/repository-name.git (fetch)
   origin    https://github.com/your-username/repository-name.git (push)
   upstream  https://github.com/original-owner/repository-name.git (fetch)
   upstream  https://github.com/original-owner/repository-name.git (push)
   ```

4. **Create a New Branch**
   ```bash
   git checkout -b jbdev
   ```

5. **Make Changes and Commit**
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

6. **Push Changes to Your Fork**
   ```bash
   git push origin jbdev
   ```

### Notes:
- **`origin`** refers to your fork of the repository.
- **`upstream`** refers to the original repository.