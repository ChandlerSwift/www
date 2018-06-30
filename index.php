<!DOCTYPE html>
<html lang="en">
<head>
    <title>Chandler Swift &ndash; developer &middot; musician &middot; student</title>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Chandler Swift—Web/desktop developer, musician, and student currently attending the University of Minnesota Duluth">
    <meta name="author" content="Chandler Swift">
    <link rel="shortcut icon" href="favicon.png">
    <link href='https://fonts.googleapis.com/css?family=Lato:300,400,300italic,400italic' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Montserrat:400,700' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="assets/plugins/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="assets/plugins/font-awesome/css/font-awesome.css">
    <link id="theme-style" rel="stylesheet" href="assets/css/styles.css">
    <link rel="apple-touch-icon" href="/favicon.png" />
</head>

<body>
    <header class="header">
        <div class="container">
            <div class="flip-container pull-left profile-image" id="flippable-profile-image">
                <div class="flipper">
                    <div class="front">
		        <img class="img-responsive" src="assets/images/profile.png" alt="Chandler Swift" title="upupdowndownleftrightrightba" />
		    </div>
                    <div class="back">
		        <img class="img-responsive" src="assets/images/profile-alt.png" alt="Chandler Swift" title="Photo creds: Isaac Swift – isaacswift.com" />
		    </div>
                </div>
            </div>
            <div class="profile-content pull-left">
                <h1 class="name">Chandler Swift</h1>
                <h2 class="desc">developer &middot; musician &middot; student</h2>
                <ul class="social list-inline">
                    <li><a href="https://github.com/ChandlerSwift"><i class="fa fa-github"></i></a></li>
                    <li><a href="https://www.linkedin.com/in/chandlerswift"><i class="fa fa-linkedin"></i></a></li>
                    <li><a href="https://stackoverflow.com/u/3814663"><i class="fa fa-stack-overflow"></i></a></li>
                    <li><a href="https://twitter.com/swftbot"><i class="fa fa-twitter"></i></a></li>
                    <li><a href="https://last.fm/user/chandlerswift"><i class="fa fa-lastfm"></i></a></li>
                    <li><a href="https://open.spotify.com/user/chandlerswift"><i class="fa fa-spotify"></i></a></li>
                    <li class="last-item"><a href="https://www.facebook.com/chandler.swift.16"><i class="fa fa-facebook"></i></a></li>
                </ul>
            </div><!--//profile-->
            <button type="button" class="btn btn-cta-primary pull-right" data-toggle="modal" data-target="#contactModal"><i class="fa fa-paper-plane"></i> Contact Me</button>
        </div><!--//container-->
    </header><!--//header-->

    <!-- Modal -->
    <div class="modal fade" id="contactModal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
            <h4 class="modal-title" id="ModalTitle">Contact Me</h4>
          </div>
          <div class="modal-body">
            <form class="form-horizontal" id="contactForm">
              <div class="form-group">
                <label for="name" class="col-sm-2 control-label">Name</label>
                <div class="col-sm-10">
                  <input type="text" class="form-control" id="name" name="name" placeholder="Your Name" required>
                </div>
              </div>
              <div class="form-group">
                <label for="email" class="col-sm-2 control-label">Email</label>
                <div class="col-sm-10">
                  <input type="email" class="form-control" id="email" name="email" placeholder="Your Email" required>
                  </div>
              </div>
              <div class="form-group">
                <label for="message" class="col-sm-2 control-label">Message</label>
                <div class="col-sm-10">
                  <textarea class="form-control" rows="4" name="message" required></textarea>
                </div>
              </div>
          </div>
          <div class="modal-footer">
            <input class="btn btn-success" type="submit" value="Send!" id="submit">
            <button class="btn" data-dismiss="modal">Cancel</a>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="container sections-wrapper">
        <div class="row">
            <div class="primary col-md-8 col-sm-12 col-xs-12">
                <section class="about section">
                    <div class="section-inner">
                        <h2 class="heading">About Me</h2>
                        <div class="content">
                            <p>First and foremost, I'm a student at the <a href="https://d.umn.edu/">University of Minnesota, Duluth</a> studying <a href="https://d.umn.edu/cs/">Computer Science</a> and a little music. I enjoy working with computers, especially in relation to Linux (currently running <strike>Ubuntu</strike> <strike>Windows 10</strike> Ubuntu GNOME) and web development (full-stack).</p>
                            <p> Musically, I like playing the piano, especially accompanying choirs (mostly high school and church). I also enjoy playing both <a href="https://www.youtube.com/watch?v=xSH4ciadjDs">piano</a> and <a href="https://www.youtube.com/watch?v=p1DxQMJe7EM">organ</a> for my church when I'm back at home, and I can occasionally be found there behind a trumpet as well. Jazz is fun. </p>
                            <p>Outside of school, I like to remain active with <a href="http://troop352.us/">my Boy Scout troop</a> (of which I am an Eagle Scout), especially on outdoor activities. I like reading science fiction, though I don't have as much time for it as I might like. I appreciate <a href="https://xkcd.com/">XKCD comics</a>, especially those about <a href="https://xkcd.com/722/">technology</a>.</p>
                        </div><!--//content-->
                    </div><!--//section-inner-->
                </section><!--//section-->

               <section class="latest section">
                    <div class="section-inner">
                        <h2 class="heading">Latest Projects</h2>
                        <div class="content">

                            <div class="item featured text-center">
                                <h3 class="title"><a href="https://github.com/ChandlerSwift/RaceClock" target="_blank">RaceClock</a></h3>
                                <p class="summary">A laser timing and tracking system for small racetracks</p>
                                <div class="featured-image">
                                    <a href="https://github.com/ChandlerSwift/RaceClock" target="_blank">
                                        <img class="img-responsive project-image" src="assets/images/projects/project-featured.jpg" alt="RaceClock" />
                                    </a>
                                    <div class="ribbon">
                                        <div class="text">New!</div>
                                        </div>
                                    </div>

                                <div class="desc text-left">
                                    <p>After a few years of frustration using stopwatches and post-it notes to <span title="haha, get it? Track?">track</span> record times on the dirt racecourse on our property, it was determined that a better solution was needed. After much deliberation, it was determined that a laser timing system with start indicator (a traffic light on loan from <a href="https://ericvillnow.com/">a friend</a>) would serve the track best. <a href="https://github.com/ChandlerSwift/RaceClock">RaceClock</a> is the result. It's powered by a Raspberry Pi (which itself is powered by a 12v battery and inverter) and automatically tracks times on its local (served over a wifi hotspot) and remote (synced to <a href="http://racing.chandlerswift.com">ChandlerSwift.com</a>) web servers.</p>
                                </div><!--//desc-->
                                <a class="btn btn-cta-secondary" href="https://github.com/ChandlerSwift/RaceClock" target="_blank"><i class="fa fa-github"></i> View on Github</a>
                            </div><!--//item-->
                            <hr class="divider" />
                            <div class="item row">
                                <a class="col-md-4 col-sm-4 col-xs-12" href="https://experiments.chandlerswift.com/piano-heatmap/" target="_blank">
                                <img class="img-responsive project-image" src="assets/images/projects/grand-piano.jpg" alt="Grand Piano" />
                                </a>
                                <div class="desc col-md-8 col-sm-8 col-xs-12">
                                    <h3 class="title"><a href="https://experiments.chandlerswift.com/piano-heatmap/" target="_blank">Piano Heatmap (An Experimental Work in Progress)</a></h3>
                                    <p>Curious which of your piano keys is most used? So was I. Meet my piano heatmap for MIDI-enabled keyboards. More information on <a href="https://blog.chandlerswift.com/2015/piano-heatmap-analysis-part-1/">this blog post</a>.</p>
                                    <p><a class="more-link" href="https://experiments.chandlerswift.com/piano-heatmap/" target="_blank"><i class="fa fa-external-link"></i> Check it out</a></p>
                                </div>
                            </div><!--//item-->
                        </div><!--//content-->
                    </div><!--//section-inner-->
                </section><!--//section-->

                <section class="projects section">
                    <div class="section-inner">
                        <h2 class="heading">Projects for my FIRST Robotics team</h2>
                        <div class="content">
                            <div class="item">
                                <h3 class="title"><a href="#">TimeClock</a> <span class="label label-theme">Open Source</span></h3>
                                <p class="summary">Tracks work hours on FRC teams via a beautiful and easy-to-navigate web interface, and allows coaches veto rights to keep hours honest. </p>
                                <p><a class="more-link" href="https://github.com/PredatorsRobotics/TimeClock" target="_blank"><i class="fa fa-external-link"></i> View on Github</a></p>
                            </div>
                            <div class="item">
                                <h3 class="title"><a href="https://github.com/PredatorsRobotics/MeetStatusScreen">MeetStatusScreen</a> <span class="label label-theme">Open Source</span></h3>
                                <p class="summary">This web application provided a convenient way to track FRC competition data. It displays a countdown until the next event, and who partners and opponents are on that event. It displays alliance color, time, and current weather conditions. </p>
                                <p><a class="more-link" href="https://github.com/PredatorsRobotics/MeetStatusScreen" target="_blank"><i class="fa fa-external-link"></i> View on GitHub</a></p>
                            </div>
                            <a class="btn btn-cta-secondary" href="http://predators4665.org">Robotics Website <i class="fa fa-chevron-right"></i></a>
                        </div>
                    </div>
                </section>

                <section class="experience section">
                    <div class="section-inner">
                        <h2 class="heading">Work Experience <a href="chandlerswift-resume-dec17.pdf">(R&eacute;sum&eacute;)</a></h2>
                        <div class="content">
                            <div class="item">
                                <h3 class="title">Web Developer &ndash; <span class="place"><a href="http://bravoreporting.com">Bravo Reporting</a></span> <span class="year">(Spring 2015 &ndash; Present)</span></h3>
                                <p>I worked with PHP and the Laravel framework to build a web application that does progress reporting with action item tracking on large projects. I also used HTML, CSS, and JavaScript to create an immersive front-end application. I worked to bring legacy code up to date with modern standards, and created documentation and unit tests for the application.</p>
                            </div><!--//item-->
                            <div class="item">
                                <h3 class="title">Technology Intern &ndash; <span class="place"><a href="http://www.gsl.k12.mn.us/pages/Glencoe_Silver_Lake_Public_Sch/District_Info/Departments/Administrative_Departments/Technology">GSL Schools</a></span> <span class="year">(2013 &ndash; 2015)</span></h3>
                                <p>My primary role was to support the district's large user base across several schools, including hardware repair and software instruction. I also performed software installations (both <a href="http://www.opsi.org/en">automated</a> and customized), and installed and configured hardware in labs throughout the district. </p>
                            </div><!--//item-->

                        </div><!--//content-->
                    </div><!--//section-inner-->
                </section><!--//section-->
            </div><!--//primary-->
            <div class="secondary col-md-4 col-sm-12 col-xs-12">
                 <aside class="info aside section">
                    <div class="section-inner">
                        <h2 class="heading sr-only">Basic Information</h2>
                        <div class="content">
                            <ul class="list-unstyled">
                                <li><i class="fa fa-map-marker"></i><span class="sr-only">Location:</span><a href="https://duluth.chandlerswift.com/">Duluth, Minnesota</a></li>
                                <li><i class="fa fa-envelope-o"></i><span class="sr-only">Email:</span><a href="mailto:chandler@chandlerswift.com">chandler@chandlerswift.com</a></li>
                                <li><i class="fa fa-link"></i><span class="sr-only">Website:</span><a href="/">chandlerswift.com</a></li>
                            </ul>
                        </div><!--//content-->
                    </div><!--//section-inner-->
                 </aside><!--//aside-->

                 <aside class="aside section">
                     <div class="section-inner">
                         <h2 class="heading">Now Playing</h2>
		         <div id="now-playing-container" class="row">
			   <p>Loading&hellip;</p>
			 </div>
                     </div>
                 </aside>

<?php /*                 <aside class="skills aside section">
                    <div class="section-inner">
                        <h2 class="heading">Skills</h2>
                        <div class="content">
                            <p class="intro">
                                I'm primarily a web developer, although lately I've been doing more work with desktop and mobile apps. I'm experienced in administering a LAMP stack, and I'm also proficient in using Office apps and many Adobe products.</p>

                            <div class="skillset">

                                <div class="item">
                                    <h3 class="level-title">PHP &amp; Laravel<span class="level-label">Expert</span></h3>
                                    <div class="level-bar">
                                        <div class="level-bar-inner" data-level="95%">
                                        </div>
                                    </div><!--//level-bar-->
                                </div><!--//item-->
                                
                                <div class="item">
                                    <h3 class="level-title">HTML5 &amp; CSS3<span class="level-label">Pro</span></h3>
                                    <div class="level-bar">
                                        <div class="level-bar-inner" data-level="85%">
                                        </div>
                                    </div><!--//level-bar-->
                                </div><!--//item-->

                                <div class="item">
                                    <h3 class="level-title">Javascript &amp; jQuery<span class="level-label">Good</span></h3>
                                    <div class="level-bar">
                                        <div class="level-bar-inner" data-level="60%">
                                        </div>
                                    </div><!--//level-bar-->
                                </div><!--//item-->

                                <div class="item">
                                    <h3 class="level-title">Python &amp; others<span style="text-decoration: underline;" class="level-label" data-toggle="tooltip" data-placement="left" data-animation="true" title="I've hacked together a few programs in a lot of languages, and I pick up new languages quickly!">Well...</span></h3>
                                    <div class="level-bar">
                                        <div class="level-bar-inner" data-level="35%">
                                        </div>
                                    </div><!--//level-bar-->
                                </div><!--//item-->
                            </div>
                        </div><!--//content-->
                    </div><!--//section-inner-->
                 </aside><!--//section--> */ ?>
                 <aside class="education aside section">
                    <div class="section-inner">
                        <h2 class="heading">Education</h2>
                        <div class="content">
                            <div class="item">
                                <h3 class="title"><i class="fa fa-graduation-cap"></i> College: Computer Science</h3>
                                <h4 class="university">University of Minnesota Duluth<br/>
                                Dean's List 6/6, Presidential Scholarship<br/>
                                <span class="year">(2015&ndash;2019)</span></h4>
                            </div><!--//item-->
                            <div class="item">
                                <h3 class="title"><i class="fa fa-graduation-cap"></i> GSL High School &ndash; Glencoe, MN</h3>
                                <h4 class="university">Honors, Engineering, Top 10%&hellip; <span class="year">(2011&ndash;2015)</span></h4>
                            </div><!--//item-->
                        </div><!--//content-->
                    </div><!--//section-inner-->
                </aside><!--//section-->

                <aside class="blog aside section">
                    <div class="section-inner">
                        <h2 class="heading">Latest Blog Posts</h2>
                        <div id="rss-feeds" class="content">
                        </div><!--//content-->
                    </div><!--//section-inner-->
                </aside><!--//section-->

                <aside class="list conferences aside section">
                    <div class="section-inner">
                        <h2 class="heading">Portfolio/Sites I Run</h2>
                        <div class="content">
                            <ul class="list-unstyled">
                                <li><a href="/" target="_blank">ChandlerSwift.com</a> &ndash; My Website</li>
                                <li><a href="https://troop352.us">Troop352.us</a> &ndash; My Scout Troop</li>
                                <li><a href="https://stjohnscccc.org">StJohnsCCCC.org</a> &ndash; My Church</li>
				<li><a href="http://jaeckelorgans.com/">JaeckelOrgans.com</a> &ndash; a local organ builder</li>
                            </ul>
                        </div><!--//content-->
                    </div><!--//section-inner-->
                </aside><!--//section-->
                
                <aside class="list conferences aside section">
                    <div class="section-inner">
                        <h2 class="heading">ChandlerSwift.com Links</h2>
                        <div class="content">
                            <ul class="list-unstyled">
                                <li><a href="https://webmail.chandlerswift.com/" target="_blank">Webmail</a></li>
                                <li><a href="https://cloud.chandlerswift.com/" target="_blank">File Storage</a> (<a href="https://owncloud.org/">OwnCloud</a>)</li>
                                <li><a href="https://cswift.tk/" target="_blank">URL Shortener</a> (<a href="https://yourls.org/">YOURLS</a>)</li>
                                <li><a href="https://experiments.chandlerswift.com/" target="_blank">Current and Archived Projects</a></li>
                                <li><a href="https://ac.cswift.tk/" target="_blank">AssaultCube Server</a></li>
				<li><a href="https://minecraft.chandlerswift.com" target="_blank">Minecraft Server</a></li>
                            </ul>
                        </div><!--//content-->
                    </div><!--//section-inner-->
                </aside><!--//section-->
            </div><!--//secondary-->
        </div><!--//row-->
    </div><!--//masonry-->

    <!-- ******FOOTER****** -->
    <footer class="footer">
        <div class="container text-center">
                <small class="copyright">&copy; 2012-2018 <a href="/">Chandler Swift</a> &ndash; Site design by <a href="http://themes.3rdwavemedia.com" target="_blank">Xiaoying Riley</a></small>
        </div><!--//container-->
    </footer><!--//footer-->

    <!-- Javascript -->
    <script type="text/javascript" src="assets/plugins/jquery-1.11.2.min.js"></script>
    <script type="text/javascript" src="assets/plugins/jquery-migrate-1.2.1.min.js"></script>
    <script type="text/javascript" src="assets/plugins/bootstrap/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="assets/plugins/jquery-rss/dist/jquery.rss.js"></script>
    <script type="text/javascript" src="assets/js/main.js"></script>
    <script>
      $("#now-playing-container").load("/now-playing.php");

      var kkeys = [], konami = "38,38,40,40,37,39,37,39,66,65";

      $(document).keydown(function(e) {
        kkeys.push( e.keyCode );
        if ( kkeys.toString().indexOf( konami ) >= 0 ) {
          kkeys = [];
          document.querySelector("#flippable-profile-image").classList.toggle("flip");
        }
      });
    </script>
</body>
</html>


