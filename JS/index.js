
let img, gray, imgManipulator, imgUtil;

let toIndex;
window.onload = ()=>{
    imgUtil = new ImageUtil();
    toIndex = imgUtil.toIndex;
    imgManipulator = new ImageManipulator();
    let canvas = document.createElement('canvas');
    document.getElementById('canvasContainer').appendChild(canvas);
    let ctx = canvas.getContext('2d');
    
    imgUtil.loadImage('https://upload.wikimedia.org/wikipedia/en/2/24/Lenna.png').then(imageData => {
        canvas.width = imageData.width;
        canvas.height = imageData.height;
        img = imageData;
        ctx.putImageData(imageData, 0, 0);
        gray = ctx.createImageData(imageData.width, imageData.height);
        gray.data.set(imageData.data)
        
        imgUtil.grayscale(gray.data);
        ctx.putImageData(gray, 0, 0);
    });
}

function histogram(){
    let canvas = document.createElement('canvas');
    let ctx = canvas.getContext('2d');
    canvas.width = 255;
    canvas.height = 100;
    scale = imgManipulator.max(gray) / canvas.height;
    document.getElementById('canvasContainer').appendChild(canvas);

    let hist = imgManipulator.histogram(gray);
    let imgData = ctx.createImageData(canvas.width, canvas.height);
    hist.forEach((item, index)=>{
        imgData.data[toIndex(index)] = item;
        imgData.data[toIndex(index) + 1] = item;
        imgData.data[toIndex(index) + 2] = item;
    })


}


// function openFile(){
//     let input = document.createElement('input');
//     input.type = 'file';
//     input.click();
//     console.log(ImageReader);
//     return new Promise(resolve=>{
//         input.addEventListener('change', (e)=>{
//             resolve(input.value);
//         })
//     });
    
// }

// function chooseFile(){
//     openFile().then(value=>{
        
//     });
// }