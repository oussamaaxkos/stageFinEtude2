const chart = document.querySelector("#chart").getContext('2d');
// create a new chart instance

new Chart(chart , {

    type:'line',
    data : {
        labels : ['Jan' , 'Feb' , 'Mar', 'Apr' , 'May' , 'Jun',
        'Jul' , 'Aug' , 'Sep' , 'Oct' , 'Nov'],

        datasets:[{
            label : 'CUSTOMERS',
            data : [20,123,2527,182736,19736 ,356 ,22633,27321,82123,2444635,1233],
            borderColor : 'red',
            borderWidth : 2
        },
     
        {
            label : 'SHOP',
            data : [220,323,2,1927,2434451 ,1244451,98297,1262524,122735,992212,1223],
            borderColor : 'blue',
            borderWidth : 2

        },
    ]
    }

})



let menuBtn = document.querySelector("#menu-btn");
let closeBtn = document.querySelector("#close-btn");
let sideBar = document.querySelector("aside");


menuBtn.addEventListener('click' , ()=>{

  sideBar.style.display = 'block';

})

closeBtn.addEventListener('click' , ()=>{

  sideBar.style.display='none';


})

const themeBtn = document.querySelector('.theme-btn');

themeBtn.addEventListener('click', ()=>{

    document.body.classList.toggle('dark-theme');
    themeBtn.querySelector('span:first-child').classList.toggle('active');

    themeBtn.querySelector('span:last-child').classList.toggle('active')

})

