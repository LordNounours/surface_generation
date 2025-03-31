import vtk
import os

def get_sorted_vtk_files(directory):
    """ Récupère et trie les fichiers .vtk d'un dossier."""
    files = [f for f in os.listdir(directory) if f.endswith(".vtk")]
    files.sort()  # Trie les fichiers par ordre alphabétique
    return [os.path.join(directory, f) for f in files]

def load_and_display_vtk(vtk_root_dir, vtk_stem_dir):
    # Récupérer et trier les fichiers .vtk
    root_files = get_sorted_vtk_files(vtk_root_dir)
    stem_files = get_sorted_vtk_files(vtk_stem_dir)
    
    # Vérifier qu'il y a bien le même nombre de fichiers
    num_files = min(len(root_files), len(stem_files))
    if num_files == 0:
        print("Aucun fichier .vtk trouvé dans les dossiers spécifiés.")
        return
    
    # Initialiser le rendu
    renderer = vtk.vtkRenderer()
    render_window = vtk.vtkRenderWindow()
    render_window.SetSize(800, 800)
    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)
    render_window.AddRenderer(renderer)
    
    for i in range(num_files):
        reader_root = vtk.vtkPolyDataReader()
        reader_root.SetFileName(root_files[i])
        reader_root.Update()
        polydata_root = reader_root.GetOutput()
        
        reader_stem = vtk.vtkPolyDataReader()
        reader_stem.SetFileName(stem_files[i])
        reader_stem.Update()
        polydata_stem = reader_stem.GetOutput()
        
        # Gestion des couleurs pour root
        colors_root = polydata_root.GetPointData().GetArray("Colors")
        color_data_root = vtk.vtkUnsignedCharArray()
        color_data_root.SetName("Colors")
        color_data_root.SetNumberOfComponents(3)
        
        if colors_root:
            for j in range(colors_root.GetNumberOfTuples()):
                r, g, b = colors_root.GetTuple(j)
                color_data_root.InsertNextTuple3(int(r * 255), int(g * 255), int(b * 255))
        else:
            for j in range(polydata_root.GetNumberOfPoints()):
                color_data_root.InsertNextTuple3(25, 25, 25)
        
        polydata_root.GetPointData().SetScalars(color_data_root)
        
        # Gestion des couleurs pour stem
        colors_stem = polydata_stem.GetPointData().GetArray("Colors")
        color_data_stem = vtk.vtkUnsignedCharArray()
        color_data_stem.SetName("Colors")
        color_data_stem.SetNumberOfComponents(3)
        
        if colors_stem:
            for j in range(colors_stem.GetNumberOfTuples()):
                r, g, b = colors_stem.GetTuple(j)
                color_data_stem.InsertNextTuple3(r,g,b)
        
        polydata_stem.GetPointData().SetScalars(color_data_stem)
        
        # Mappers
        mapper_root = vtk.vtkPolyDataMapper()
        mapper_root.SetInputData(polydata_root)
        
        mapper_stem = vtk.vtkPolyDataMapper()
        mapper_stem.SetInputData(polydata_stem)
        
        # Actors
        actor_root = vtk.vtkActor()
        actor_root.SetMapper(mapper_root)
        actor_root.GetProperty().SetOpacity(0.1)
        
        actor_stem = vtk.vtkActor()
        actor_stem.SetMapper(mapper_stem)
        actor_stem.GetProperty().SetOpacity(1.0)
        
        # Assembly
        assembly = vtk.vtkAssembly()
        assembly.AddPart(actor_root)
        assembly.AddPart(actor_stem)
        
        renderer.AddActor(assembly)
    
    # Configuration finale
    renderer.SetBackground(0.0, 0.3, 0.5)
    renderer.ResetCamera()
    
    # Interaction
    """style = vtk.vtkInteractorStyleTrackballActor()
    render_window_interactor.SetInteractorStyle(style)"""
    
    render_window.Render()
    render_window_interactor.Start()

if __name__ == "__main__":
    # Définir les dossiers des fichiers root et stem
    root_dir = "/home/caro/Documents/Ressources/Annotation_plante_01/mesh/leaf/cylinder_reduced/"
    stem_dir = "/home/caro/Documents/Ressources/Annotation_plante_01/mesh/leaf/stem_reduced/"
    
    # Lancer l'affichage
    load_and_display_vtk(root_dir, stem_dir)
