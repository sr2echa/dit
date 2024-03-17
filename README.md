> [!NOTE]
> The Dit project has been published on [Pypi](https://pypi.org/project/dbdit/). You can install it using pip.

![image](https://github.com/sr2echa/dit/assets/65058816/791a94a6-2d97-4f10-9c02-d40f664db196)

Dit revolutionizes database management by introducing a version control system tailored specifically for databases, akin to Git's role in source code management. It directly addresses a significant pain point in developer workflows: the complex and error-prone process of tracking, merging, and reverting database schema and content changes. By automating and streamlining these tasks, Dit significantly enhances developer productivity in several key areas:

**Seamless Integration with DevOps Pipelines:** Dit integrates into existing development workflows, allowing database changes to be versioned, reviewed, and deployed alongside application code. This tight integration reduces friction and improves the speed of development cycles.

**Conflict Resolution and Collaboration:** Dit's intelligent merge conflict resolution facilitates smoother collaboration among team members working on the same database. By providing clear, manageable mechanisms to handle conflicts, Dit minimizes downtime and communication overhead, allowing developers to focus on their core tasks.

**Environment Consistency:** Dit ensures that all team members and deployment environments are synchronized with the latest database changes, mitigating "it works on my machine" issues and streamlining the deployment process across development, staging, and production environments.

**Rapid Rollbacks and Historical Analysis:** The ability to quickly revert to previous database states or analyze the history of changes empowers developers to troubleshoot and fix issues faster, further boosting productivity.

**Enhanced Data Management:** For projects involving data analysis or machine learning, Dit provides version control for datasets, enabling more efficient experimentation and collaboration on data-driven projects.

By providing a robust, intuitive tool for database version control, Dit fills a crucial gap in the modern developer's toolkit, making database-related tasks safer, faster, and more collaborative. This contributes significantly to the developer productivity track by reducing manual overhead, speeding up development cycles, and fostering better collaboration and consistency across projects.

# 🦄 Installation
#### 1. Clone the repo
```
git clone https://github.com/sr2echa/dit.git
```
#### 2. Install the requirements
```
pip install -r requirements.txt
```
#### 3. Install Dit
```
pip install .
```

# ✨ Useage

<samp>

```
 Dit                                                                                  
 Dit is a version control system for your databases.

╭─ Commands ─────────────────────────────────────────────────────────────────────────╮
│ branch        Create a new branch from the current commit.                         │
│ commit        Commit your database changes                                         │
│ diff          Compare the current database with a specific commit hash.            │
│ init          Initialize Dit Repository                                            │
│ log           Shows the commit log of the dit repo                                 │
│ merge         Merge a branch into the current branch.                              │
│ reset         Reset the database to a specific state by commit hash.               │
╰────────────────────────────────────────────────────────────────────────────────────╯
```

</samp>
