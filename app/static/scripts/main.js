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

// Skills
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

// Experience tabs
const tabs= document.querySelectorAll('[data-target]')
const tabContents= document.querySelectorAll('[data-content]')

tabs.forEach(tab => {
    tab.addEventListener("click", () => {
        const target = document.querySelector(tab.dataset.target);
        
        tabContents.forEach(tabContent => {
            tabContent.classList.remove('experience-active')
        })

        target.classList.add('experience-active');

        tabs.forEach(tab => {
            tab.classList.remove('experience-active')
        })

        tab.classList.add('experience-active')
    })
})