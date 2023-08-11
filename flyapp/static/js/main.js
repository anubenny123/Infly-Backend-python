const link1 = document.getElementById('svg1');
const svg1 = document.getElementById('dropicon');
const boxes = document.getElementsByClassName('incheight');
const hello = document.getElementsByClassName('test');
const items = document.getElementsByClassName('item1');
const itempic = document.getElementsByClassName('itempic');
const sec3 = document.getElementsByClassName('sec3full');
const feedback = document.getElementById('feedbackbtn');
const products = document.getElementById('products');
const mobilediv = document.getElementById('mbdiv');
const offerBtn = document.getElementById('offerbtn');
const aboutus = document.querySelector('.aboutus');
const feed = document.querySelector('.feed');
const popup = document.getElementById('popup');
const mobilenav = document.getElementById('mob');
const overlay = document.createElement('div');
let hiddenboxID;
const x = boxes.length;
const y = items.length;

link1.addEventListener('mouseover', () => {
  svg1.classList.add('svghover');
});

link1.addEventListener('mouseout', () => {
  svg1.classList.remove('svghover');
});

const handleMouseOver = (index) => {
  hello[index].classList.add('height');
};

const handleMouseOut = (index) => {
  hello[index].classList.remove('height');
};

for (let i = 0; i < x; i++) {
  boxes[i].addEventListener('mouseover', () => {
    handleMouseOver(i);
  });

  boxes[i].addEventListener('mouseout', () => {
    handleMouseOut(i);
  });
}

for (let j = 0; j < y; j++) {
  items[j].addEventListener('mouseover', () => {
    itempic[j].classList.add('box-shadow');
  });

  items[j].addEventListener('mouseout', () => {
    itempic[j].classList.remove('box-shadow');
  });
}


function openDetails(id) {
  const details = document.getElementsByClassName('purchase-details');
  for (let i = 0; i < details.length; i++) {
    details[i].classList.remove('width');
  }
  hiddenboxID = id;
  const hiddenbox = document.getElementById(`hiddenbox${id}`);
  if (window.innerWidth < 930) {
    hiddenbox.classList.add('w-100');
  } else {
    hiddenbox.classList.toggle('width');
  }
}


mobilenav.addEventListener('click', (event) => {
  mobilediv.classList.toggle('h-auto');
  event.stopPropagation();
});

document.addEventListener('click', () => {
  mobilediv.classList.remove('h-auto');
});

document.addEventListener('click', (event) => {
  const clickedElement = event.target;
  const sideNav = document.getElementById(`hiddenbox${hiddenboxID}`);

  // Check if the clicked element is within the side navigation or its child elements
  if (!sideNav.contains(clickedElement)) {
    closeNav();
  }
  if (!popup.contains(event.target)) {
    popup.classList.remove('click');
  }
  if (!products.contains(event.target)) {
    products.classList.remove('opacity');
  }
});

function hideProducts(event) {
  products.classList.toggle('opacity');
  event.stopPropagation();
}

function closeNav(id) {
  hiddenboxID = id;
  const hiddenbox = document.getElementById(`hiddenbox${id}`);
  if (hiddenbox.classList.contains('w-100')) {
    hiddenbox.classList.remove('w-100');
  } else {
    document.getElementById(`hiddenbox${id}`).classList.remove('width');
  }
}

function closeExp() {
  popup.classList.remove('click');
  try {
    document.body.removeChild(overlay);
  }catch(err) {
  console.log(err)
}
}

feedback.addEventListener('click', (event) => {
  event.stopPropagation();
  popup.classList.toggle('click');
  document.body.appendChild(overlay);
});
document.querySelector('#rate').addEventListener('click',()=>{
  event.stopPropagation();
  popup.classList.toggle('click');
  document.body.appendChild(overlay);
})

popup.addEventListener('click', (event) => {
  event.stopPropagation();
});

overlay.classList.add('overlay');

overlay.addEventListener('click', () => {
  popup.classList.remove('click');
  document.body.removeChild(overlay);
});

if(window.innerWidth < 930){
  document.querySelector('.sec2main').insertBefore(aboutus , feed)
  document.querySelector('.newsh1').innerHTML = 'Stay Up-to-Date with Our Monthly Newsletter';
}