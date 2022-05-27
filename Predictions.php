<!DOCTYPE HTML>
<html>

<head>
  <title>Predictions</title>
  <meta name="description" content="website description" />
  <meta name="keywords" content="website keywords, website keywords" />
  <meta http-equiv="content-type" content="text/html; charset=windows-1252" />
  <link rel="stylesheet" type="text/css" href="style/style.css" />
</head>

<body>
  <div id="main">
  <div id="header">
      <div id="logo">
        <!-- class="logo_colour", allows you to change the colour of the text -->
        <h1><a href="index.php">Intrusion Detection System</span></a></h1>
        <h2>With machine learning and data analysis</h2>
      </div>
      <<div id="menubar">
        <ul id="menu">
          
        <li ><a href="index.php">Home</a></li>
          <li><a href="Pie.php">Pie Chart</a></li>
          <li><a href="Heat.php">Heat Map</a></li>
          <li><a href="Predictions.php">Predictions</a></li>
          <li><a href="contact.php">Contact Us</a></li>
        </ul>
      </div>
    </div>
    <div id="site_content">
   <div class="sidebar">
        
        <h1>Useful Links</h1>
        <ul>
        <li><a href="https://www.machinelearningplus.com/time-series/arima-model-time-series-forecasting-python/">Arima Model</a></li>
          <li><a href="https://scapy.readthedocs.io/en/latest/usage.html">Scapy</a></li>
          <li><a href="https://en.wikipedia.org/wiki/Intrusion_detection_system">What is IDS?</a></li>
          <li><a href="https://towardsdatascience.com/what-is-feature-engineering-importance-tools-and-techniques-for-machine-learning-2080b0269f10#:~:text=Feature%20engineering%20is%20the%20process,design%20and%20train%20better%20features">Feature Engineering</a></li>
        </ul>
     
      </div>
      <div id="content">
        <h1>Predictions</h1>
         
        <form method="POST" action="#">
        <button name="start" type="submit" class="button" >Start Analyzing</button>
        <button name="gen" type="submit" class="button" >Show Prediction</button>
        </form>

        <br>
        <br>
        <hr>
        <?php
        $dirname = "data/AI/";
        $images = glob($dirname."*.*");

        foreach($images as $image) {
        ?>
        <div class="images">
          <img src="<?php echo $image; ?>" height="200px">
          <center><h3><?php echo $image; ?></h3></center>
        </div>
        <br><br>
        <hr>
        <?php
        }
        ?>
       
        
      </div>
    </div>
    
  </div>
<script src="Script/Dalmakhni.js"></script>
</body>
</html>

<?php

function execInBackground($cmd) { 
  if (substr(php_uname(), 0, 7) == "Windows"){ 
      pclose(popen("start /B ". $cmd, "r"));  
  } 
  else { 
      exec($cmd . " > /dev/null &");   
  } 
}

if(isset($_POST['start']))
{
  execInBackground('start cmd.exe @cmd /k "python python/CleanAgr.py"');  
  echo "
  <script>
  window.location.href = 'Predictions.php';
  </script>
  ";
}

if(isset($_POST['gen']))
{
  execInBackground('start cmd.exe @cmd /k "python python/AI.py"'); 
  echo "
  <script>
  window.location.href = 'Predictions.php';
  </script>
  ";
}
?>