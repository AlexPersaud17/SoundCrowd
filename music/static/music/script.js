$(document).ready(function(){
  if(['/music/album/all/', '/music/album/add/'].includes(window.location.pathname)){
    $(".navbar").addClass("navbar-shrink")
  }
})