<?php
  $api_key = rtrim(file_get_contents('../lastfm-api-key.txt'));
  $track = json_decode(file_get_contents('http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=chandlerswift&api_key='.$api_key.'&format=json&limit=1'))->recenttracks->track[0];
?>
<div class="row">
  <div class="col-xs-4">
    <img style="max-width:100%" src="<?php echo $track->image[2]->{'#text'} ?>" />
  </div>
  <div class="col-xs-8">
    <b><a href="<?php echo $track->url ?>">
        <?php echo $track->name ?>
    </a></b>
    <p><?php echo $track->artist->{'#text'} ?></p>
    <p><?php echo $track->album->{'#text'} ?></p>
  </div>
</div>
