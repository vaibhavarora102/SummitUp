window.addEventListener('scroll',()=>{
    document.querySelector('nav').classList.toggle('window-scrolled',window.scrollY > 0)
})

function searchResults(){
    document.getElementById("searchbarparent").style.padding=0;

    document.getElementById("searchbarchild").style.marginTop=0;
    
    document.getElementById("results").style.display="block";
}

setTimeout(function(){
    document.getElementById("headingtop").style.display="none";
    document.getElementById("maindiv").style.display="block";
},3000);

$('#i_file').change( function(event) {
    var tmppath = URL.createObjectURL(event.target.files[0]);
    $("img").fadeIn("fast").attr('src',URL.createObjectURL(event.target.files[0]));
    
    $("#disp_tmp_path").html("Temporary Path(Copy it and try pasting it in browser address bar) --> <strong>["+tmppath+"]</strong>");
});