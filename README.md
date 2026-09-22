# Oryx with custom QMK

This repository allows combining the convenience of [Oryx’s](https://www.zsa.io/oryx) graphical layout editing with the power of [QMK](https://qmk.fm), allowing you to customize your Oryx layout with advanced QMK features like Achordion and Repeat Key, while automating firmware builds through GitHub Actions.

For a detailed guide, check out the full [blog post here](https://blog.zsa.io/oryx-custom-qmk-features).

## How it works

Each time you run the GitHub Action, the workflow will:
1. Fetch the latest changes made in Oryx.
2. Merge them with any QMK features you've added in the source code.
3. Build the firmware, incorporating modifications from both Oryx and your custom source code.

## How to use

1. Fork this repository (be sure to **uncheck the "Copy the main branch only" option**).
2. To initialize the repository with your layout:
   - Go to the **Actions** tab.
   - Select **Fetch and build layout**.
   - Click **Run workflow**.
   - Input your layout ID and keyboard type (your layout must be public in Oryx), then run the workflow.
   - (To avoid having to input values each time, you can modify the default values at the top of the `.github/workflows/fetch-and-build-layout.yml` file).
3. A folder containing your layout will be generated at the root of the repository.
4. You can now add your custom QMK features to this folder:
   - Edit `config.h`, `keymap.c` and `rules.mk` according to the [QMK documentation](https://github.com/qmk/qmk_firmware/tree/master/docs/features).
   - Commit and push to the **main** branch.
5. You can continue editing your layout through Oryx:
   - Make your changes in Oryx. 
   - Optionally, add a description of your changes in the **Some notes about what you changed** field; if provided, this will be used as commit message.
   - Confirm changes by clicking the **Compile this layout** button.
6. To build the firmware (including both Oryx and code modifications), rerun the GitHub Action. The firmware will be available for download in the action’s artifacts.
7. Flash your downloaded firmware using [Keymapp](https://www.zsa.io/flash#flash-keymap).
8. Enjoy!

## Oryx Chrome extension

To make building even easier, [@nivekmai](https://github.com/nivekmai) created an [Oryx Chrome extension](https://chromewebstore.google.com/detail/oryx-extension/bocjciklgnhkejkdfilcikhjfbmbcjal) to be able to trigger the GitHub Actions from inside Oryx itself.


## This fork: ZGMw7 and custom gaming chat

Run **Fetch and build layout** on **main**, with `ZGMw7` and `voyager`.
Edit normal key assignments in Oryx, compile there, then run this workflow.
Flash the GitHub artifact to retain custom features.

- `oryx` must contain only Oryx-generated layout files. Never merge `main`
  into `oryx`, and never put custom code there.
- `main` owns `ZGMw7/gaming_chat.h` and the small include/call in `keymap.c`.
- Keep Gaming/G2/Gaming Chat at layers 1/2/3. Keep F24 on G2 and **plain
  Enter and Escape** on Gaming Chat, without hold actions. Set these plain
  keys in Oryx too; the repaired main already has them.
- The existing Q/K and E/J dual functions, including their 20 ms tap delays,
  remain in `keymap.c`. Oryx should use those same tap/hold assignments.
- The validator stops the build if the chat hook, header, or required keys
  disappear. It cannot verify the human names of layers or physical behavior.

### Resolve conflicts only on main

Do not use GitHub's **Resolve conflicts** on a PR from `oryx` to `main`:
that can merge `main` into the source branch and contaminate `oryx`.
Instead, with a clean local working tree:

```sh
git switch main
git pull --ff-only origin main
git fetch origin oryx
git merge origin/oryx
# Resolve keymap.c, retaining Oryx key changes and the custom hook.
python scripts/validate_layout.py ZGMw7
git add ZGMw7/keymap.c
git commit
git push origin main
```

Then rerun the workflow on main. Never force-push or reset the oryx history
as part of routine conflict resolution. Its current files are already a pure
export; the historical accidental merge does not need to be rewritten.
