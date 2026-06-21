# Aditri Growth Portfolio Project

## Phase 1: Environment Setup

## Tools Installed

- Cursor IDE
- Git
- GitHub
- Claude Code extension (attempted) 
- Codex extension (attempted)

## Steps Completed

1. Created a GitHub account and a public repository called `Aditri-Growth-Portfolio`.
2. Downloaded and installed Cursor IDE.
3. Connected my GitHub account to Cursor.
4. Downloaded and installed Git.
5. Opened the repository folder in Cursor.
6. Created and edited this README file.
7. Verified that Git was installed correctly using terminal commands.

## Issues I Ran Into and How I Solved Them

### Issue 1: Cloning the repository directly in Cursor

**Problem:**  

I was unable to clone the repository directly through Cursor initially.

**Solution:**  

I downloaded the repository as a ZIP file from GitHub and opened the folder manually in Cursor so I could continue working without getting blocked.

### Issue 2: Finding files and navigating Cursor

**Problem:**  

As a first-time Cursor user, I had difficulty locating the file explorer and understanding the interface.

**Solution:**  

I explored the menus and found the file explorer under **View > Files**, which allowed me to access and edit project files.

### Issue 3: Git commands were not recognized

**Problem:**  

After installing Git, commands such as `git add .` returned an error indicating that Git was not recognized.

**Solution:**  

I learned that Cursor needed to be restarted after the installation. After reopening Cursor and creating a new terminal session, Git was detected successfully.

### Issue 4: Repository was not initialized

**Problem:**  

When I ran Git commands, I received the error: `fatal: not a git repository (or any of the parent directories): .git`

**Solution:**  

I learned that a folder must first be connected to a Git repository. Creating the GitHub repository and configuring Git locally helped me understand the relationship between local and remote repositories.

### Issue 5: Git required an identity before committing

**Problem:**

When attempting to create a commit, Git returned an "Author identity unknown" error and would not proceed.

**Solution:**

I learned that Git requires a username and email address to be configured before commits can be created. I configured my Git identity through the terminal and was then able to commit my changes successfully.

### Issue 6: Push to GitHub was rejected

**Problem:**

My initial push to GitHub was rejected because the remote repository already contained content that was not present in my local copy.

**Solution:**

I learned how local and remote repositories can become out of sync. I pulled the remote changes, completed the merge process, and then successfully pushed my local changes to GitHub.

### Issue 7: Claude Code and Codex extension installation

**Problem:**

- Claude Code extension was not visible in the Cursor marketplace.
- Located alternative installation methods through Anthropic documentation, but installation failed due to a VS Code compatibility error.
- Attempted installation through the `cursor:extension/anthropic.claude-code` protocol link, which also failed.
- Researched the issue and found reports of compatibility problems between certain Cursor versions and the Claude Code extension.
- Codex-related searches similarly returned no compatible installation options within the current Cursor environment.
- Documented the issue and proceeded with the remaining setup steps.

**Solution:**

I researched the issue, tested multiple installation approaches, and reviewed available documentation. Although I was unable to install the extensions successfully, I documented the problem and the troubleshooting steps taken. This experience reinforced the importance of systematic troubleshooting and clear documentation when a technical issue cannot be resolved immediately.

# What I Learned

This project gave me my first hands-on experience with GitHub, Git, and AI-powered development tools.

Key learnings include:

- How GitHub repositories are created and managed
- The difference between local folders, Git repositories, and remote repositories
- How Git commands such as `git init`, `git add`, `git commit`, `git pull`, and `git push` work together
- How Git integrates with development environments like Cursor
- How to troubleshoot installation, configuration, and compatibility issues
- How repository synchronization issues can occur and how to resolve them
- The importance of documenting technical problems and the steps taken to solve them
- The value of researching independently and testing multiple solutions when encountering technical blockers
- How AI tools can assist with learning and problem-solving during unfamiliar tasks

One thing that stood out to me during this project was that technical work rarely goes exactly as planned. Several parts of the setup process did not work on the first attempt, including Git configuration, repository setup, synchronization issues, and attempts to install the Claude Code and Codex extensions. Each problem required a different approach, and solving them involved a combination of research, experimentation, and persistence.

Although I come from a non-technical background, this exercise showed me that most technical challenges can be solved by breaking them into smaller steps, searching for reliable information, and methodically troubleshooting each issue. It also reinforced the importance of staying patient when things do not work immediately.

Overall, this project gave me practical exposure to GitHub, Git, Cursor, and technical troubleshooting, while helping me become more confident in learning new tools independently.  

## Phase 2: LinkedIn Organic Content Strategy Research

### Project Goal

The goal of this phase was to understand how successful B2B SaaS operators use LinkedIn to build audiences, generate demand, strengthen positioning, and create pipeline.

Rather than collecting generic marketing advice, I focused on identifying repeatable frameworks, content systems, distribution strategies, and growth mechanisms used by practitioners actively building SaaS businesses.

### Experts Researched

I selected 10 operators with different strengths across B2B SaaS growth:

1. Adam Robinson
2. Amanda Natividad
3. Nick Bennett
4. Justin Welsh
5. Jasmin Alić
6. Katelyn Bourgoin
7. Tommy Clark
8. Anthony Pierri
9. Des Traynor
10. Lukas Hermann

### Data Collection Process

#### Step 1: Source Selection

I identified long-form interviews, podcasts, educational videos, and public content from each operator.

#### Step 2: Transcript Retrieval

I created a Python script (`scripts/fetch_transcripts.py`) and used the Supadata API to retrieve transcript data from YouTube videos.

The transcripts were stored inside:

`research/youtube-transcripts/`

#### Step 3: Research Organization

I organized the collected materials into separate folders for:

- Source documentation
- Transcript archives
- Individual operator playbooks

This made it easier to analyze each operator independently and keep the repository structured.

#### Step 4: Strategic Synthesis

I reviewed the transcript data and extracted:

- Positioning frameworks
- Content operating systems
- Distribution strategies
- Demand generation approaches
- Growth playbooks
- Decision-making principles

The findings were documented in:

`research/linkedin-posts/`

### Repository Structure

#### Sources

Contains the master research catalog with links, notes, and selection rationale for each expert.

Location:

`research/sources.md`

#### LinkedIn Playbooks

Contains individual research summaries and framework breakdowns for all 10 operators.

Location:

`research/linkedin-posts/`

#### Transcript Archive

Contains the raw transcript files collected during the research process.

Location:

`research/youtube-transcripts/`

#### Retrieval Script

Contains the Python script used to retrieve transcript data.

Location:

`scripts/fetch_transcripts.py`

### Challenges I Ran Into and How I Solved Them

#### Challenge 1: Retrieving Transcript Data at Scale

Problem:

Manually copying long-form transcript content would have been slow and difficult to maintain.

Solution:

I created a Python-based workflow using the Supadata API to retrieve transcript data programmatically and store it directly inside the repository.

#### Challenge 2: Separating Signal from Noise

Problem:

Long-form interviews contain a mixture of stories, opinions, and actionable frameworks.

Solution:

I focused only on concrete systems, positioning frameworks, operating principles, distribution strategies, and growth mechanisms that could be supported by transcript evidence.

#### Challenge 3: Maintaining Consistency Across 10 Operators

Problem:

Each operator discusses different topics and uses different terminology.

Solution:

I standardized every research file using the same structure so that strategies could be compared across operators more easily.

### Key Takeaways

Across all 10 operators, the strongest LinkedIn strategies were built around:

- Clear positioning
- Deep audience understanding
- Consistent content distribution
- Demand creation over lead chasing
- Repeatable content systems rather than individual viral posts

### Outcome

This repository contains:

- 10 researched B2B SaaS operators
- Annotated source documentation
- Transcript archive
- Strategic playbooks derived from transcript analysis
- A custom transcript retrieval script

The final result is a structured research dataset that can be used as the foundation for a future LinkedIn Organic Growth Playbook for B2B SaaS companies.