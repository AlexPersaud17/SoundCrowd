$(document).ready(function(){
  console.log(window.location.pathname)
  var urls_shrink_nav = ['/music/register/', '/music/login/', '/music/album/all/', '/music/album/add/'];
  if($.inArray(window.location.pathname, urls_shrink_nav ) > -1){
    $(".navbar").addClass("navbar-shrink")
  }
})