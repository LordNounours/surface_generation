import vtk
import os

def get_sorted_vtk_files(directory):
    """
    Retrieves and sorts .vtk files from a directory.
    """
    files = [f for f in os.listdir(directory) if f.endswith(".vtk")]
    files.sort()  # Sort files alphabetically
    return [os.path.join(directory, f) for f in files]

def decimate_polydata(polydata, reduction=0.5):
    """
    Reduces the number of triangles in a polydata mesh.

    Args:
        polydata (vtkPolyData): Input polydata.
        reduction (float): Fraction of triangles to remove (0.0 - 1.0).

    Returns:
        vtkPolyData: Simplified polydata.
    """
    decimate = vtk.vtkDecimatePro()
    decimate.SetInputData(polydata)
    decimate.SetTargetReduction(reduction)  
    decimate.PreserveTopologyOff()
    decimate.Update()
    
    return decimate.GetOutput()

def save_vtk_polydata(polydata, output_path):
    """
    Saves a polydata mesh to a .vtk file.
    """
    writer = vtk.vtkPolyDataWriter()
    writer.SetFileName(output_path)
    writer.SetInputData(polydata)
    writer.Write()

def process_vtk(root_dir, stem_dir, output_root_dir, output_stem_dir, reduction=0.5):
    """
    Processes VTK files by reducing the mesh complexity and saving the results.

    Args:
        root_dir (str): Directory containing root VTK files.
        stem_dir (str): Directory containing stem VTK files.
        output_root_dir (str): Output directory for processed root files.
        output_stem_dir (str): Output directory for processed stem files.
        reduction (float): Reduction factor for mesh decimation.
    """
    # Ensure output directories exist
    os.makedirs(output_root_dir, exist_ok=True)
    os.makedirs(output_stem_dir, exist_ok=True)

    # Retrieve and sort .vtk files
    root_files = get_sorted_vtk_files(root_dir)
    stem_files = get_sorted_vtk_files(stem_dir)
    
    # Ensure there are files to process
    num_files = min(len(root_files), len(stem_files))
    if num_files == 0:
        print("No .vtk files found in the specified directories.")
        return

    for i in range(num_files):
        # Read the root VTK file
        reader_root = vtk.vtkPolyDataReader()
        reader_root.SetFileName(root_files[i])
        reader_root.Update()
        polydata_root = reader_root.GetOutput()

        # Read the stem VTK file
        reader_stem = vtk.vtkPolyDataReader()
        reader_stem.SetFileName(stem_files[i])
        reader_stem.Update()
        polydata_stem = reader_stem.GetOutput()

        # Reduce mesh complexity
        polydata_root = decimate_polydata(polydata_root, reduction)
        polydata_stem = decimate_polydata(polydata_stem, reduction)

        # Save reduced meshes
        root_filename = os.path.basename(root_files[i])
        stem_filename = os.path.basename(stem_files[i])
        save_vtk_polydata(polydata_root, os.path.join(output_root_dir, root_filename))
        save_vtk_polydata(polydata_stem, os.path.join(output_stem_dir, stem_filename))

if __name__ == "__main__":
    # Input directories
    root_dir = "/home/caro/Documents/Ressources/Annotation_plante_01/mesh/root/test2_cylinder/"
    stem_dir = "/home/caro/Documents/Ressources/Annotation_plante_01/mesh/root/test2_stem/"

    # Output directories
    output_root_dir = "/home/caro/Documents/Ressources/Annotation_plante_01/mesh/root/test2_cylinder_reduced/"
    output_stem_dir = "/home/caro/Documents/Ressources/Annotation_plante_01/mesh/root/test2_stem_reduced/"

    # Process the VTK files with a 90% reduction in complexity
    process_vtk(root_dir, stem_dir, output_root_dir, output_stem_dir, reduction=0.9)
