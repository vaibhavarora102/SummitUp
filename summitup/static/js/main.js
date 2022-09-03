window.addEventListener('scroll',()=>{
    document.querySelector('nav').classList.toggle('window-scrolled',window.scrollY > 0)
})

function searchResults(){
    document.getElementById("searchbarparent").style.padding=0;

    document.getElementById("searchbarchild").style.marginTop=0;
    
    document.getElementById("results").style.display="block";
}

setTimeout(function(){
    $("#headingtop").fadeOut(300);
},3000);