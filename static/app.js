const searchBar = document.getElementById('search-bar');
const searchButton = document.getElementById('search-button');
const search = document.getElementById('search');
const searchForm = document.getElementById('search-form')
const char_profile_div = document.getElementById('char_profile_div');
const strength = document.getElementById("strength");
const dexterity = document.getElementById('dexterity-div');
const constitution = document.getElementById('constitution-div');
const race = document.getElementById("race");
const stat_array = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']
const half_elf = document.getElementsByClassName("race");
const scores_and_modifiers = {'-5':[0,1], '-4':[2,3], '-3':[4,5], '-2':[6,7], '-1':[8,9], '0':[10,11], '1':[12,13], '2':[14,15], '3':[16,17], '4':[18,19], '5':[20,21], '6':[22,23], '7':[24,25], '8':[26,27], '9':[28,29], '10':[30,31]};
const base_url = 'https://www.dnd5eapi.co/api/';
const armor = document.getElementById('armor');
const char_class = document.getElementById('character_class');
const browseButton = document.getElementById("browse");
const flashMessage = document.getElementById('flash_message');


// window.onload = function() {
//     if (screen.width <= 400) {
//         searchButton.classList.add('hidden');
//         browseButton.classList.add('hidden');
//         welcomeDiv = document.getElementsByClassName("welcome-div");
//         let msg_div = document.createElement('div');
//         msg_div.innerText = "This website is not intended to be used on a mobile device, so it will have limited functionality"
//         msg_div.setAttribute("class", "noMobile");
//         welcomeDiv[0].append(msg_div);
//         if (flashMessage) {
//         flashMessage.classList.add('hidden');
//         };
//     }
// }






search.addEventListener("click", (evt) => {
    //adds an event listener to the search button so that when it is clicked it will remove the hidden class from the bar and allow a user to search users and characters
    evt.preventDefault();
    searchBar.classList.toggle('hidden')
    searchButton.classList.toggle('hidden')
    searchForm.classList.toggle('hidden')
})

async function getAbilityScores(stat_name, stat_value) {
    //iterates through the scores_and_modifiers object and returns the corresponding key for the values and then assigns that to a new div and paragraph, appending it to the page
    let stats_div = document.getElementById(`${stat_name}-div`);
    let newPara = document.createElement('p');
    newPara.classList = "modifiers";
    const mods = Object.entries(scores_and_modifiers)
    for (let i = 0; i < mods.length; i++) {
    if (mods[i][1].includes(parseInt(stat_value))) {
        let statValue = parseInt(mods[i][0])
        if (statValue > -1) {
        newPara.innerText = `+ ${statValue.toString().split('').join(' ')} `;

    } else {newPara.innerText = `${statValue.toString().split('').join(' ')} `};

    stats_div.append(newPara);

    } } }


char_profile_div.addEventListener("load", race_modifiers(race));

async function race_modifiers(char_race) {
// gets the race of the character and calls the dnd api so to get the racial stat bonuses and then loops through the stats and adjusts stats accordingly
    let lowCase = char_race.value.toLowerCase();
    let resp = await axios.get(`${base_url}races/${lowCase}`);
    let new_stat = resp.data.ability_bonuses;

    if (lowCase == 'half-elf') {
        newDiv = document.createElement('div')
        newDiv.innerText = 'Note: Half-Elf gets +1 to two other stats';
        newDiv.classList = "half-elf"
        half_elf[0].append(newDiv)
    }

    for (let base of stat_array) {
        let ability = document.getElementById(`${base}`);
        let ability_name = ability.id;
        let trunc_ability = ability_name.slice(0, 3);

        for (let stat of new_stat) {
            index = stat.ability_score['index'];
            if (index === trunc_ability) {
                if (parseInt(ability.value) > -1) {
                    ability.style = "color:green";
                ability.value = parseInt(ability.value) + parseInt(stat.bonus);
                }
                else {
                    ability.value = parseInt(ability.value) + parseInt(stat.bonus);
                    ability.style = "color:red";
                }
            } 
        }
        getAbilityScores(ability.id, ability.value);
    } armor_class(armor); get_hitpoints(char_class.value)
  }

async function armor_class(armor) {
    
    armor_resp = await axios.get(`${base_url}equipment/${armor.value}`);
    base = armor_resp.data.armor_class['base'];
    bonus = armor_resp.data.armor_class['dex_bonus'];
    dex_div = dexterity.firstElementChild.innerText;
    new_num = dex_div.split(' ')[1];
    newDiv = document.createElement('p');
    newDiv.classList = "modifiers";
    myDiv = document.getElementById('armor_class-div');    
    
    if (bonus) {
        myArmor = base + parseInt(new_num);
        newDiv.innerText = myArmor;
        myDiv.appendChild(newDiv);
    } else {
        newDiv.innerText = base;
        myDiv.appendChild(newDiv);        
    };


}

async function get_hitpoints(class_name) {
    lowCase = class_name.toLowerCase();
    resp = await axios.get(`${base_url}classes/druid`);
    hit_die = resp.data.hit_die;
    newDiv = document.createElement('p');
    newDiv.classList = 'modifiers';
    con_div = constitution.firstElementChild.innerText;
    new_num = con_div.split(' ')[1];
    console.log(new_num)
    hitpoints = parseInt(new_num) + hit_die;
    newDiv.innerText = hitpoints;
    hit_points_div = document.getElementById('hit_points-div');
    hit_points_div.append(newDiv);
}



// const statsDiv = document.getElementById("stats")
// const char_class = document.getElementById("character_class")




// const base_stats = () => {
//     // creates a vertical list of base stats and creates a dropdown selection from 1 to 18 for each stat
//     const stats = ['Strength', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma', 'Dexterity']
//     for (let stat of stats) {
//         let newDiv = document.createElement('div');
//         newDiv.innerText = `${stat}:  `;
//         newDiv.classList = 'newDiv';
//         newDiv.id = stat;
//         statsDiv.append(newDiv);
//         let contents = "<option>1</option>"
//         let newSelect = document.createElement('select');
//         newDiv.append(newSelect);
//         for (let i = 2; i < 19; i++) {
//             contents += "<option>" + i + "</option>";
//         }
//         newSelect.innerHTML = contents
//     }
    
// }


// adds event listener so that when the class changes, the hitpoints change....but don't need it anymore...
// char_class.addEventListener("change", (evt) => {
//     get_hit_die(evt.target.value);
//     console.log('test')
// })

//async fxn that will call the api to get the hit-die for the class that is chosen, might use this for exporting to pdf to calculate chosen max hit points
// async function get_hit_die(dice) {
//     classname = dice.toLowerCase()
//     resp = await axios.get(`https://www.dnd5eapi.co/api/classes/${classname}`)
//     dice_sides = resp.data.hit_die;
//     console.log('test1')
//     hitpoints(dice_sides)   
// }

//populates the dropdown menu with 1 to some number, depending on how high the hit-die goes...don't need anymore...
// function hitpoints(hitdie) {
//     console.log('test1.5')
//     defaultOption = document.getElementById("default-option");
//     let contents = "<option>1</option>"
//     for (let i = 2; i < hitdie+1; i++) {
//         contents += "<option>" + i + "</option>";      
//     }
//     defaultOption.innerHTML = contents;
//     console.log('test2')

// }

// async function hitpoints(hitdie) {

// }

// const hitpoints_default() {
    
// }
// async function get_weapons() {}
// async function get_armor() {}



