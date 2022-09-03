window.addEventListener('scroll',()=>{
    document.querySelector('nav').classList.toggle('window-scrolled',window.scrollY > 0)
})



setTimeout(function(){
    $("#headingtop").fadeOut(300);
},3000);