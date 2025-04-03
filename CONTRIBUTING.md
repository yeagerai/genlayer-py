# Contributing to GenLayerPY SDK

We're thrilled that you're interested in contributing to the GenLayerPY SDK! This document will guide you through the contribution process.

## What is the GenLayerPY SDK?

The GenLayerPY SDK is a Python library designed for developers building decentralized applications (Dapps) on the GenLayer protocol. It provides a comprehensive set of tools to interact with the GenLayer network, including client creation, transaction handling, event subscriptions, and more, all while leveraging the power of web3.py as the underlying blockchain client.

## How You Can Contribute?

Contributions to the GenLayerPY SDK are welcome in several forms:

### Testing the SDK and Providing Feedback

Help us make the SDK better by testing and giving feedback:

- Start by installing the SDK in your Dapp using the command:
  ```sh
  $ pip install genlayer-py
  ```
- Try out the SDK features and tell us what you think through our [feedback form](https://docs.google.com/forms/d/1IVNsZwm936kSNCiXmlAP8bgJnbik7Bqaoc3I6UYhr-o/viewform) or on our [Discord Channel](https://discord.gg/8Jm4v89VAu).
- If you find any issues, please report them on our [GitHub issues page](https://github.com/yeagerai/genlayer-py/issues).

### Sharing New Ideas and Use Cases

Have ideas for new features or use cases? We're eager to hear them! But first:

- Ensure you have the SDK installed to explore existing use cases.
- After familiarizing yourself with the SDK, contribute your unique use case and share your ideas in our [Discord channel](https://discord.gg/8Jm4v89VAu).

### Bug fixing and Feature development

#### 1. Set yourself up to start coding

- **1.1. Pick an issue**: Select one from the project GitHub repository [issue list](https://github.com/yeagerai/genlayer-py/issues) and assign it to yourself.

- **1.2. Create a branch**: create the branch that you will work on by using the link provided in the issue details page (right panel at the bottom - section "Development")

- **1.3. Setup the SDK locally**: clone the repository

   ```sh
   $ git clone https://github.com/yeagerai/genlayer-py.git
   ```

- **1.4. Add the package to your project locally**: to add the package locally, use the command:
  - **Option 1:** Install the package in regular mode
      ```sh
      $ pip install path/to/genlayer-py
      ```
  - **Option 2:** Install the package in editable mode

      ```sh
      $ pip install -e path/to/genlayer-py --config-settings editable_mode=strict
      ```
   This will allow you to use the package in your project without publishing it. With option 1 you need to re-install the package on every changes you make and with option 2 you only need to perform a re-installation if you change the project metadata. You can find more information in the pip [documentation](https://pip.pypa.io/en/stable/topics/local-project-installs/)


#### 2. Submit your solution

- **2.1. Black Formatter on Save File**: Configure IDE extensions to format your code with [Black](https://github.com/psf/black/) before submitting it.
- **2.2. Code solution**: implement the solution in the code.
- **2.3. Pull Request**: Submit your changes through a pull request (PR). Fill the entire PR template and set the PR title as a valid conventional commit.
- **2.4. Check PR and issue linking**: if the issue and the PR are not linked, you can do it manually in the right panel of the Pull Request details page.  
- **2.5. Peer Review**: One or more core contributors will review your PR. They may suggest changes or improvements.
- **2.6. Approval and Merge**: After approval from the reviewers, you can merge your PR with a squash and merge type of action.


### Improving Documentation

To contribute to our docs, visit our [Documentation Repository](https://github.com/yeagerai/genlayer-docs) to create new issues or contribute to existing issues.

## Community

Connect with the GenLayer community to discuss, collaborate, and share insights:

- **[Discord Channel](https://discord.gg/8Jm4v89VAu)**: Our primary hub for discussions, support, and announcements.
- **[Telegram Group](https://t.me/genlayer)**: For more informal chats and quick updates.

Your continuous feedback drives better product development. Please engage with us regularly to test, discuss, and improve the GenLayerPY SDK.