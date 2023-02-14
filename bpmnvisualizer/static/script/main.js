const loader = new PIXI.Loader();

// list of variables that should be created (under some conditions)
let toGenerateList = [];

// list of variables that should be deleted (when they end move)
let toDeleteList = [];
let removedList = [];

// variable for destinations for all parts on field
destinations = {};

// variable for all parts moving around
let parts = {};

// variable for main canvas
let mainApp = undefined


// --- --- adding main canvas --- ---
function generateNewCanvas(modelName) {
    console.log(`asdasd: ${modelName}`);
    console.log(`dsadas: ${getUrlNewModel(modelName)}`);
    // define background picture
    fetch(getUrlNewModel(modelName))
    .then(response => {
        if(response.headers.get("content-type") == 'image/png') {
             resetAll = true;
            // clear previous canvas
            if (mainApp != undefined){
                document.body.removeChild(mainApp.view);
            };
            return response.blob();
        } else {
            return 'nop';
        };
    })
    .then(result => {
        if(result != 'nop'){



            var blobURL = URL.createObjectURL(result);

            var img = new Image();
            img.addEventListener("load", (event) => {
                var texture = new PIXI.Texture(new PIXI.BaseTexture(img));


                let background = new PIXI.Sprite(texture);
                background.scale.set(scale, scale);
                console.log(`width: ${background.width}`);

                // create new canvas
                mainApp = new PIXI.Application( {width: background.width, height: background.height, transparent: true });
                document.body.appendChild(mainApp.view);

                // set background picture
                mainApp.stage.addChild(background);

                mainApp.ticker.add(tick);
            });
            img.src = blobURL;


        } else {
            console.log('noop');
        }
    });

}




// loading image for parts
const partTexture = PIXI.Texture.from(part_path);

// function for generating path
function generate(x, y, name){
  let part = new PIXI.Sprite(partTexture);
  part.anchor.set(0);
  part.x = x;
  part.y = y;
  part.name = name;
  part.scale.set(0.5, 0.5);
  part.currDist = undefined;
  part.movePart = movePart;
  part.remove = remove;
  part.isRemove = false;
  mainApp.stage.addChild(part);
  return part;
}

// function for deleting part (called from inside part object as self.remove())
function remove(){
  console.log(`>>> ${this.name} was removed!!!`);
  mainApp.stage.removeChild(this);
  removedList.push(this.name);
  delete parts[this.name];
  
}

// moving part
function movePart() {
  if (this.currDist == undefined){
    this.currDist = (destinations[this.name] ?? undefined).shift();
  }
  if (this.currDist != undefined){
    let len = Math.sqrt(Math.pow((this.currDist.x - this.x), 2) + Math.pow((this.currDist.y - this.y), 2));
    if (len <= speed){
      this.x = this.currDist.x;
      this.y = this.currDist.y;
      this.currDist = undefined;
      // console.log(`${this.name} came to ${this.x};${this.y}`);
    } 
    else {
      this.x += (this.currDist.x - this.x) / (len / speed);
      this.y += (this.currDist.y - this.y) / (len / speed);
    }
  } else if (this.isRemove) {
    this.remove();
  }
}


function tick(delta) {
    // if model is not reseted
    if (!resetAll){
        // generate all that need be generated
        let i = 0, len = toGenerateList.length;
        while (i < len){
            let elem = toGenerateList.shift();
            let toAdd = true;
            for (oldName of elem.old) {
                if (!(removedList.includes(oldName))){
                    toAdd = false;
                    break;
                }
            }
            if (toAdd) {
                let part = generate(elem.x, elem.y, elem.name);
                parts[elem.name] = part;
            }
            else {
                toGenerateList.push(elem);
            }

            i += 1;
        }
        // move all that need to be moved
        Object.entries(parts).forEach(([k,v]) => {
            v.movePart();
        })
        // delete all that need to be deleted
        i = 0, len = toDeleteList.length;
        while (i < len){
            let elem = toDeleteList.shift();
            let isDeleted = false;
            let element = parts[elem] ?? undefined;
            if (!(element == undefined)){
                element.isRemove = true;
                isDeleted = true;
            }
            if (!isDeleted){
                toDeleteList.push(elem);
            }
            i += 1;
        }
    }
    // if need to reset whole model
    else {
        toGenerateList = [];
        toDeleteList = [];
        destinations = {};
        for (p in parts) {
            parts[p].remove();
        }
        resetAll = false;
    }

}

// add ticker that moves all parts every tick


// function for moving part for one step (called from inside part object as self.makeStep())
function makeStep(step){
  switch (step['type']) {
      case 'generate':
        console.log(`generating ${step['name']}`);
        toGenerateList.push({
          name: step['name'],
          x: (step['coords']['x']) * scale,
          y: (step['coords']['y']) * scale,
          old: step['old_names']
        })
        break;

      case 'move':
        // console.log(`moving ${step['name']} to ${step['to']['x']}|${step['to']['y']}`);
        if (!(step['name'] in destinations)) {
          destinations[step['name']] = [];
        }
        destinations[step['name']].push({x:(step['to']['x']) * scale, y:(step['to']['y']) * scale});
        break;

      case 'delete':
        console.log(`deleting ${step['name']}`);
        toDeleteList.push(step['name']);
        break;

      default:
        console.log('unknown command')
        break;

      }
}


function stats(){
    fetch(URLSTATS)
    .then( res => res.blob() )
    .then( blob => {
        var a = document.createElement("a");
        a.href = window.URL.createObjectURL(blob);
        a.download = "data.json";
        a.click();
    });
}


generateNewCanvas(`default`);

