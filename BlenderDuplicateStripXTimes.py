import bpy

def move_playhead_and_duplicate(duplicated_times):
    # Ensure we are in the Video Sequence Editor
    if bpy.context.scene.sequence_editor is None:
        print("No sequence editor found.")
        return

    # Get the selected strips
    selected_strips = bpy.context.selected_sequences

    if not selected_strips:
        print("No strip selected.")
        return

    # Get the correct area and region for the Video Sequence Editor
    area = next((area for area in bpy.context.screen.areas if area.type == "SEQUENCE_EDITOR"), None)
    if not area:
        print("No Video Sequence Editor found.")
        return

    # Find the correct region within the area
    region = next((region for region in area.regions if region.type == "WINDOW"), None)
    if not region:
        print("No region found in the SEQUENCE_EDITOR area.")
        return

    # Override context to ensure proper context for VSE operations
    override_context = bpy.context.copy()
    override_context["area"] = area
    override_context["region"] = region

    # Variable to track the number of duplications
    total_duplicated = 0

    # Loop to perform duplications
    while total_duplicated < duplicated_times:
        # Move the playhead forward by one frame
        bpy.context.scene.frame_current += 1

        # Perform the copy and paste operation within the overridden context
        with bpy.context.temp_override(**override_context):
            bpy.ops.sequencer.copy()
            bpy.ops.sequencer.paste()

        total_duplicated += 1
        print(f"Duplicated strip {total_duplicated}, moved playhead to frame {bpy.context.scene.frame_current}.")

        # After every 127 duplications, create a meta strip and reset channel management
        if total_duplicated % 127 == 0:
            create_meta_strip(area, region)
            select_first_strip()  # Ensure the first strip in channel 1 is selected again

            # Perform 126 more duplications after creating a meta strip
            for _ in range(126):
                bpy.context.scene.frame_current += 1
                with bpy.context.temp_override(**override_context):
                    bpy.ops.sequencer.copy()
                    bpy.ops.sequencer.paste()
                total_duplicated += 1
                print(f"Duplicated strip {total_duplicated}, moved playhead to frame {bpy.context.scene.frame_current}.")

                if total_duplicated >= duplicated_times:
                    break  # Exit if the total duplications have been reached

            # Only create another meta strip if there's more than 127 strips to go
            if total_duplicated < duplicated_times and total_duplicated % 127 == 0:
                create_meta_strip(area, region)

    print(f"Completed {duplicated_times} duplications.")

def create_meta_strip(area, region):
    # Select all strips in channels 2-128 (excluding channel 1)
    strips_to_group = [strip for strip in bpy.context.scene.sequence_editor.sequences_all if 2 <= strip.channel <= 128]
    
    if len(strips_to_group) > 0:
        # Override context to ensure proper context for VSE operations
        override_context = bpy.context.copy()
        override_context["area"] = area
        override_context["region"] = region

        # Temporarily override the context and create the meta strip for all selected strips
        with bpy.context.temp_override(**override_context):
            # Ensure all strips are selected before creating the meta strip
            for strip in strips_to_group:
                strip.select = True
            bpy.ops.sequencer.meta_make()

        print(f"Created a meta strip for channels 2-128.")

def select_first_strip():
    # Find the first strip in channel 1
    first_strip = next((strip for strip in bpy.context.scene.sequence_editor.sequences_all if strip.channel == 1), None)

    if first_strip:
        # Deselect all strips
        for strip in bpy.context.scene.sequence_editor.sequences_all:
            strip.select = False

        # Select the first strip in channel 1 explicitly
        first_strip.select = True
        bpy.context.scene.sequence_editor.active_strip = first_strip  # Set active strip to first strip in channel 1
        print(f"Selected the first strip in channel 1: {first_strip.name}")
    else:
        print("No first strip found in channel 1.")


# Run the function with the desired number of duplications
duplicated_times = 600  # Change this number to the desired times to duplicate
move_playhead_and_duplicate(duplicated_times)
