# def save_results_to_file(file_paths, output_file, batch_size=500):
#     """Saves the list of found file paths to a text file in batches."""
#     try:
#         with open(output_file, 'w') as f:
#             for i in range(0, len(file_paths), batch_size):
#                 f.writelines(f"{path}\n" for path in file_paths[i:i+batch_size])
#         logging.info(f"Saved {len(file_paths)} file paths to {output_file}")
#     except Exception as e:
#         logging.error(f"Error saving results to file {output_file}: {e}")
        
        
        
        # TODO: Error checking
        # Save the found files to a text file
        # output_file = "../search_results.txt"
        # save_results_to_file(found_files, output_file)