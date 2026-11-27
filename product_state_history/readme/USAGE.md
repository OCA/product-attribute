1. Assign users to the **Change Product State** group (Settings › Users).
2. Open a product template.
3. The state status bar is visible but not clickable.
4. Click **Change State**. This button is only visible to members of that group.
5. Select the new state and enter a reason.
6. Confirm. The product state is updated and a line is added to **State History**.

The history is available:

- as a smart button that opens the full history list

Direct writes of the state (including imports or RPC) are blocked unless a reason is provided through the same mechanism as the wizard.

Creating a product still assigns the default state without a history line. Only later changes are tracked.

Internal users can read history. Only members of **Change Product State** can create history entries through the wizard. Product State Managers can also edit or delete history records.
