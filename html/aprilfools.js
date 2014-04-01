var AprilFools = {

    setField: function(name, value) {
        var element = document.getElementById(name);
        if (element) {
            element.innerHTML = "";
            element.appendChild(document.createTextNode(value));
            return true;
        }
        return false;
    },

    randInt: function(lower, upper) {
        return lower + Math.floor((upper - lower + 1) * Math.random());
    },
    
    randIntStr: function(lower, upper, mindigits) {
        var str = "" + this.randInt(lower, upper);
        if (str.length < mindigits) {
            return Array(mindigits - str.length + 1).join("0") + str;
        } else {
            return str;
        }
    },
    
    randTimeStr: function() {
        // Nachmittagszeiten sind plausibler :p
        return this.randIntStr(16, 23, 2) + ":" + this.randIntStr(0, 59, 2);
    },
    
    nowStr: function() {
        var date = new Date();
        var hours = date.getHours();
        if (hours < 10) hours = "0" + hours;
        var hours = date.getHours();
        var minutes = date.getMinutes();
        if (minutes < 10) minutes = "0" + minutes;
        return hours + ":" + minutes;
    },

    /*        n##n,
     *        /" /##
     * YAY!  (__/ ##_   ___
     *          |    ```   `\
     *          \   /  /    |\
     *          || /_,-\   / #
     *          |||     >> >
     *         //_(    //_(     (ASCII art by jgs)
     */
    firstNames: ["Apple", "Berry", "Big", "Blue", "Caramel", "Carrot", "Cheese", "Cloudy", "Clover", "Coco", "Daring", "Diamond", "Fancy", "Filthy", "Flash", "Golden", "Granny", "Hayseed", "Lightning", "Marble", "Maud", "Pinky", "Pumpkin", "Rainbow", "Red", "Sapphire", "Shining", "Silver", "Sunset", "Sweetie", "Trixie", "Twilight"],
    secondNames: ["Bell", "Blitz", "Bloom", "Blueblood", "Cake", "Cupcake", "Fever", "Fritter", "Gala", "Hooves", "Horseshoe", "Inception", "Jubilee", "Lulamoon", "Orange", "Pie", "Pommel", "Sandwich", "Sauce", "Shill", "Shimmer", "Shores", "Sparkle", "Tiara", "Velvet"],
    
    initNames: function() {
        var firstName = this.firstNames[this.randInt(0, this.firstNames.length - 1)];
        var secondName = this.secondNames[this.randInt(0, this.secondNames.length - 1)];
        this.fullName = firstName + " " + secondName;
        this.ircNick = firstName + secondName;
        if (Math.random() < 0.8) {
            this.ircNick += this.randIntStr(0, 99, 2);
        }
        this.setField("fakename", this.fullName);
    },

    addWebChat: function() {
        // diverse Anpassungen, u. a. kein Prompt zur Registrierung des Nicknames
        var iframeSrc = "https://qchat1.rizon.net/?channels=whfspieltpokemon&prompt=1&uio=MT1mYWxzZSY2PWZhbHNlJjk9MjM0JjE2PWZhbHNl37";
        if (this.ircNick) {
            iframeSrc += "&nick=" + encodeURIComponent(this.ircNick);
        }
        var frameElem = document.createElement("iframe");
        frameElem.setAttribute("src", iframeSrc);
        frameElem.setAttribute("width", "500");
        frameElem.setAttribute("height", "378");
        frameElem.setAttribute("frameborder", "0");
        document.getElementById("therump").appendChild(frameElem);
    },
    
};


document.cookie="visited_pokemon=true";

window.addEventListener("load", function() {
    AprilFools.setField("fakecount", AprilFools.randIntStr(1, 999, 0));
    AprilFools.setField("faketime", AprilFools.randTimeStr());
    AprilFools.setField("realtime", AprilFools.nowStr());
    AprilFools.initNames();
    AprilFools.addWebChat();
});
