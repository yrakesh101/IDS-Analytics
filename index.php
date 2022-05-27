<?php
if(!isset($_COOKIE["run"]))
{
  setcookie("run", "OFF");
}
?>
<!DOCTYPE HTML>
<html>

<head>
  <title>Index</title>
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
      <div id="menubar">
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
        <h1>Welcome to IDS analytics </h1>
        <p>Aiming to build an open source IDS which could detect the packets which don't follow the rules provided by the 
          network admin, and save the details in the log file and database for future audits. Later with the help of AI models, 
          predict the frequency of forthcoming violation of rules.</p>
       
        <h2>This site feature</h2>
        <ul id="dishes">
           <li><a href="Pie.php">Show pie chart</a></li>
           <li><a href="Heat.php">Show heat map</a></li>
           <li><a href="Predictions.php">Show predictions</a></li>
        </ul>
      </div>
      <br>
      <h2>Sniffer</h2>
      <form method="POST" action="#">
        <button name="invoke" type="submit" class="button" >Run</button>
        
    </form>
    </div>

    
  </div>
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

if(isset($_POST['invoke']))
{
  execInBackground('start cmd.exe @cmd /k "python python/sniff.py"');  
  setcookie("run", "ON");
}

if(isset($_POST['terminate']) and $_COOKIE["run"]=="ON")
{
  execInBackground('start cmd.exe @cmd /k "python python/terminate.py"'); 
  setcookie("run", "OFF");
  echo "
  <script>
  window.location.href = 'index.php';
  </script>
  ";
}
if(isset($_POST['terminate']) and $_COOKIE["run"]=="OFF")
{
  echo "<script>
  alert('Sniffer is not started yet. So unable to terminate');
  window.location.href = 'index.php';
  </script>";
}
?>