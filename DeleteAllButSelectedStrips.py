import bpy

def delete_all_except_selected():
    # Ensure we are in the Video Sequence Editor
    if bpy.context.scene.sequence_editor is None:
        print("No sequence editor found.")
        return

    # Get the selected strips
    selected_strips = bpy.context.selected_sequences

    if not selected_strips:
        print("No strip selected.")
        return

    # Get all strips in the sequence
    all_strips = bpy.context.scene.sequence_editor.sequences_all

    # Deselect all strips first to avoid accidental deletion
    bpy.ops.sequencer.select_all(action='DESELECT')

    # Loop through all strips and select those that are not selected
    for strip in all_strips:
        if strip not in selected_strips:
            strip.select = True  # Select the strip to delete

    # Now delete the selected strips
    bpy.ops.sequencer.delete()

    print("All unselected strips have been deleted.")

# Run the function
delete_all_except_selected()
