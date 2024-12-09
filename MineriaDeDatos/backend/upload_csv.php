<?php
// Verificar si se ha subido un archivo
if ($_SERVER['REQUEST_METHOD'] == 'POST' && isset($_FILES['csvFile'])) {
    $fileName = $_FILES['csvFile']['name'];
    $fileTmpName = $_FILES['csvFile']['tmp_name'];
    $filePath = '../uploads/' . $fileName;

    // Mover el archivo CSV a la carpeta de uploads
    if (move_uploaded_file($fileTmpName, $filePath)) {
        // Ejecutar el script Python para analizar el CSV
        $command = escapeshellcmd("python ../python/analyze_csv.py $filePath");
        $output = shell_exec($command);

        // Mostrar el resultado del análisis
        echo "<h2>Resultados del Análisis:</h2>";
        echo "<pre>$output</pre>";

        // Verificar si existen los archivos HTML generados por Python
        $outputDir = '../python/output/';
        if (is_dir($outputDir)) {
            $files = scandir($outputDir);
            echo "<h4>Gráficos Generados:</h4>";
            foreach ($files as $file) {
                if (strpos($file, '.html') !== false) {
                    echo "<a href='../python/output/$file' target='_blank'>Ver gráfico: $file</a><br>";
                }
            }
        }
    } else {
        echo "Error al subir el archivo CSV.";
    }
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSV Checker - Plataforma Educativa</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="index.html">Plataforma Educativa</a>
        </div>
    </nav>

    <div class="container mt-5">
        <h2 class="text-center">Analizador de Archivos CSV</h2>
        <p class="text-center">Sube un archivo CSV para verificar su integridad y analizar su contenido.</p>

        <form action="upload_csv.php" method="POST" enctype="multipart/form-data" class="mt-4">
            <div class="mb-3">
                <label for="csvFile" class="form-label">Archivo CSV</label>
                <input type="file" class="form-control" id="csvFile" name="csvFile" required>
            </div>
            <button type="submit" class="btn btn-primary">Subir y Analizar</button>
        </form>
    </div>
</body>
</html>
