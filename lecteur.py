def get_html(title, liste):
    return f"""<!DOCTYPE html>
<html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body{"{"}
                display: flex;
                flex-direction: column;
                align-items: center;
            {"}"}
            .horizon{"{"}
                display: flex;
                flex-direction: row;
                justify-content: space-evenly;
                width: 100%;
            {"}"}
            .verticale{"{"}
                display: flex;
                flex-direction: column;
                align-items: center;
            {"}"}
        </style>
    </head>
    <body onload="load();">
        <div class="horizon">
            <button onclick="PreChap();">Précédent</button>
            <select id="select" onchange="selectChap();">
                <option value="1">Chapitre 1</option>
            </select>
            <button onclick="NextChap();">Suivant</button>
        </div>
        <div class="verticale">

        </div>
        <script>
            var chap = {liste};
            var imgs = document.querySelector(".verticale");
            var select = document.getElementById("select");
            var select_chap = undefined;
            function place() {"{"}
                imgs.innerHTML = "";
                for (let i = 1; i <= chap[select_chap]; i++) {"{"}
                        var img = document.createElement("img");
                        img.src = `${"{"}select_chap{"}"}/${"{"}i{"}"}.jpg`;
                        imgs.appendChild(img);
                        
                    {"}"}
            {"}"}
            function load() {"{"}
                select.innerHTML = "";
                chap.forEach((n, i, arr) => {"{"}
                    if (n != 'a') {"{"}
                        var op = document.createElement("option");
                        op.value = i;
                        op.innerText = "Chapitre " + i;
                        select.appendChild(op);
                        if (select_chap == undefined) {"{"}
                            select_chap = i;
                        {"}"}
                    {"}"}
                {"}"});
                place();
            {"}"}
            function NextChap() {"{"}
                if (chap[select_chap + 1]) {"{"}
                    select_chap++;
                    select.value = select_chap;
                    place();
                {"}"}
            {"}"}
            function PreChap() {"{"}
                if (chap[select_chap - 1]) {"{"}
                    select_chap--;
                    select.value = select_chap;
                    place();
                {"}"}
            {"}"}
            function selectChap() {"{"}
                select_chap = select.value;
                place();
                
            {"}"}
    </script>
    </body>
</html>"""