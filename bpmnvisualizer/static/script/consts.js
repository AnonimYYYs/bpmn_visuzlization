const buttonStepText = 'Сделать шаг';
const buttonResetText = 'Сбросить модель';
const buttonModelText = 'Новая модель';
const buttonStatsText = 'Выгрузить статистику';
let speed = 3;
let scale = 1;
let part_path = 'static/pics/part_images/part1.png';






const graphics = new PIXI.Graphics();

let resetAll = false;

function getUrlStep(n=1){
    return `${URLSTEP}${n}`;
}

function getUrlNewModel(model='default') {
    return `${URLNEWMODEL}${model}`;
}