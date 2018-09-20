# Contributing


**We appreciate all kinds of help, so thank you!**

## Contributing to the project

You can contribute in many ways to this project.

### Issue reporting

This is a good point to start when you find a problem, please add
it to the `issue tracker <https://github.com/GarridoLabs/test-textgenrnn>`_.
The ideal report should include the steps to reproduce it.

### Doubts solving

To help less advanced users is another wonderful way to start. You can
help us close some opened issues. This kind of tickets should have the label ``type: question``.

### Improvement proposal

If you have an idea for a new feature, please open a ticket labeled as
``type: enhancement`` or ``type: feature request``. If you could also add a piece of code with the idea or partial implementation, it would be awesome.


## Good first contributions

You are welcome to contribute wherever in the code you want to, of course, but we recommend taking a look at the "Good first contribution" label into the issues and pick one. We would love to mentor you!

## Doc

Review the parts of the documentation regarding the new changes and update it if it's needed.

## Pull requests

We use `GitHub pull requests <https://help.github.com/articles/about-pull-requests>`_ to accept the contributions.

A friendly reminder! We'd love to have a previous discussion about the best way to implement the feature/bug you are contributing to. This is a good way to improve code quality in our beloved CLI!, so remember to file a new Issue before starting to code for a solution.

So after having discussed the best way to land your changes into the codebase, you are ready to start coding (yay!). We have two options here:

1. You think your implementation doesn't introduce much code, right?. Ok, no problem, you are all set to create the PR once you have finished coding.  We are waiting for it!
2. Your implementation does introduce many things in the codebase. That sounds great! Thanks!. In this case, you can start coding and create a PR with the word: **[WIP]** as a prefix of the description and the label `status: WIP/WAITING`. This means "Work In Progress", and allow reviewers to make micro reviews from time to time without waiting to the big and final solution... otherwise, it would make reviewing and coming changes pretty difficult to accomplish. The reviewer will remove the **[WIP]** prefix from the description once the PR is ready to merge.

Please follow the next rules for the commit messages:

- It should include a reference to the issue ID in the first line of the commit, **and** a brief description of the issue, so everybody knows what this ID refers to without wasting to much time on following the link to the issue.

- It should provide enough information for a reviewer to understand the changes and their relation to the rest of the code.

A good example:

.. code::

    Issue #190: Short summary of the issue
    * One of the important changes
    * Another important change

A (really) bad example:

.. code::

    Fixes #190

## Development cycle

Our development cycle is straightforward, we define a roadmap using the Github project with milestones for the releases, and features that we want to include in these releases. The roadmap is not entirely public at the moment, but it's a committed project in our community, and we are working to make parts of it public in a way that can be beneficial for everyone. Whenever a new release is close to being launched, we'll announce it and detail what has changed since the latest version. The channels we'll use to announce new releases are still being discussed, but for now, you can follow this repo!

### Branch model

We use the [Github Flow model](https://guides.github.com/introduction/flow/), so:

- ``master``

  - This is the branch that originates the releases.
  - You should expect this branch to be frequently updated.

- Other branches

  - Will be created to develop new features, enhancements or bug fixes
  - Will be merged in the `master` branch through a PR and removed after merging the branch.


To get (most possible) stable versions of this CLI, retrieve that from the [releases](https://github.com/GarridoLabs/test-textgenrnn/releases)


### Release cycle

From time to time, we will release brand new versions of the `test-textgenrnn`. These are well-tested versions of the software.

When it is necessary to release a new version, we follow the Semantic Versioning and this process:

1. Create a new pull request
  * Title: Prepare release `vMAJOR.MINOR.PATCH`
  * Changes:
    * Update the project version number.
      * For example, the version of the package.json
      * Update the CHANGELOG.md file: Move the content from the Unreleased section to a new version section as Keep a Changelog suggest.

2. Merge the pull request
  * All the GitHub checks must pass satisfactorily.
3. Publish a new GitHub release (/releases/new)
  * Version: `vMAJOR.MINOR.PATCH`
  * Title: Same as version
  * Description: Copy the content of the new version section from the `CHANGELOG.md` file.

### What version should I use?

Master, always master to begin the development.

## Documentation

For the moment, the documentation is compiled in the `README.md` and in this `CONTRIBUTING.md`.

## Developing code for test-textgenrnn

This section includes some tips that will help you to develop code for this CLI.

### Style guide
To be defined our own style guide, but we like those defined by *TBD*


### How to run locally the project

TBD

### Development setup

TBD


### Configuring Python >3.5

The code has some previous requirements, one of them is Python 3.5 or higher.

#### MacOS X

If there are no XCode command line tools installed:

```
xcode-select --install
```

It is recommended to continue using [Homebrew](https://brew.sh/index_es) as a package manager.

```
brew install python3
cd <your-directory>
python3 -m venv <your-virtual-env>
source <your-virtual-env>/bin/activate
```

Some additional information can be found in this [link](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos).

Also, you can use a conda distribution https://conda.io/docs/user-guide/getting-started.html