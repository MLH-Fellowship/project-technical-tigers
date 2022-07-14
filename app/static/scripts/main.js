const navMenu = document.getElementById('nav-menu');
const navToggle = document.getElementById('nav-toggle');
const navClose = document.getElementById('nav-close');
const navLink = document.querySelectorAll('.nav-link');
const scrollUp= document.getElementById('scroll-up');

if(navToggle){
    navToggle.addEventListener('click', () =>{
        navMenu.classList.add('show-menu')
    })
}

if(navClose){
    navClose.addEventListener('click', () =>{
        navMenu.classList.remove('show-menu')
    })
}

navLink.forEach(n => n.addEventListener('click', ()=>{
    navMenu.classList.remove('show-menu')
}))

const scrollUpEvent = () =>{
    if(this.scrollY >= 50){
        scrollUp.classList.add('show-scroll')
    }else{
        scrollUp.classList.remove('show-scroll');
    } 
}

window.addEventListener('scroll', scrollUpEvent);

const skillsContent = document.getElementsByClassName("skills-content");
const skillsHeader = document.querySelectorAll(".skills-header");

function toggleSkills(){
    let itemClass = this.parentNode.className
    for(i = 0; i < skillsContent.length; i++){
        skillsContent[i].className = 'skills-content skills-close'
    }

    if (itemClass === 'skills-content skills-close'){
        this.parentNode.className = 'skills-content skills-open'
    }
}

skillsHeader.forEach((element) =>{
    element.addEventListener("click", toggleSkills)
})