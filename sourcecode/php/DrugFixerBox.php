<html>  
<body>
<br>
<br>
<br>

<?php

	if ($_SERVER['REQUEST_METHOD'] != "POST") {
		echo '<form action="DrugFixerBox.php" method="post">
			Drug Name: <input type="text" name="fixword" autofocus><br>
			<input type="submit">
		</form>
		<br>
		<br>';


	} else  {
		include 'NorvigSpellCorrector.php';
		#$pspell = pspell_new('en','canadian','','utf-8',PSPELL_FAST);

		$fixword = $_POST['fixword'];

		//Drug Name: <input type="text" name="fixword" value='.$fixword.' autofocus><br>
		echo '<form action="DrugFixerBox.php" method="post">
			Drug Name: <input type="text" name="fixword" autofocus><br>
			<input type="submit">
		</form>
		<br>
		<br>';

	
		$candidates = NorvigSpellCorrector::correct($fixword, True);

		if (count($candidates) == 0) {
			echo '<h2> "'.$fixword.'" has no good matches. </h2>';
		} else {


			echo '<h2> The best match to "'.$fixword.'" is: </h2>';
			echo '<ul>';
			echo '<li>'.NorvigSpellCorrector::correct($fixword).'</li>';
			echo '</ul>';



			if (count($candidates) > 1) {
				echo '<h2> The available candidates: </h2>';
				echo '<ul>';

				foreach ($candidates as $c) {
					echo '<li>'.$c.'</li>';
				}
			}
		}

		echo '</ul>';
	}

?>

</body>

</html>  
