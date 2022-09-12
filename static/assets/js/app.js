// NEW STUFF HERE
// const keywords = new Map([
//     ["guide", "Beginner's guide"],
//     ["diabetes", "What is diabetes?"],
//     ["type1", "Type 1"],
//     ["type2", "Type 2"],
//     ["gestational", "Gestational"],
//     ["long term", "Long term negative effects"],
//     ["treatment", "type 1 treatment options"],
//     ["type 2 treatment", "type 2 treatment options"],
//     ["diet", "Healthy eating"],
//     ["daily", "recommended daily routine"],
//     ["help", "tips and tricks"],
//     ["tips", "tips and tricks"]
// ]);

const keywords = new Map([
    // ["guide", "Beginner's guide"],
    ["what is diabetes", "what"],
    ["type", "types"],
    ["types", "types"],
    ["type1", "type 1"],
    ["type2", "type 2"],
    ["type 1", "type 1"],
    ["type 2", "type 2"],
    ["gestational", "gestational"],
    // ["long term", "Long term negative effects"],
    // ["treatment", "type 1 treatment options"],
    // ["type 2 treatment", "type 2 treatment options"],
    // ["diet", "Healthy eating"],
    // ["daily", "recommended daily routine"],
    // ["help", "tips and tricks"],
    // ["tips", "tips and tricks"]
    ["?help", "?help"],
    ["?diet", "?diet"],
    ["?treament", "?treatment"]
]);
// NEW STUFF ENDS HERE

const info_map = new Map([
    ["what", "Diabetes occurs when your blood glucose from the food you eat becomes too high. Insulin helps move glucose from our bloodstream into the body's cells to make energy but for some individuals, the pancreas does not make enough or use insulin well."],
    ["types", "There are 3 main types, type 1, type 2 and gestational diabetes, all being complex and serious."],
    ["type 1", "Type 1 diabetes is a chronic medical condition where cells that make insulin are destroyed, hence the body is unable to process glucose due to the lack of insulin."],
    ["type 2", "Type 2 diabetes is a chronic medical condition where your body is not able to respond to insulin as well as it should. In later stages, it also many not produce enough insulin. When uncontrolled, may lead to chronically high blood glucose levels, leading to serious complications."],
    ["gestational", "Gestational diabetes typically develops between the 24th to 28th week of pregnancy. Although not indicative of having diabetes before or after pregnancy, it raises the risk of type 2 diabetes in the future. If poorly managed, it can raise the child's chance of developing diabetes and create complications during pregnancy and delivery."],
    ["?help", "Available commands: ?diet, ?treatment"],
    ["?diet", "//Healthy eating is essential etc. LINK HERE//"],
    ["?treatment", "//Explore your treatment options here, includes all types of diabetes. LINK HERE//"]
])

const info_list = [
    "Diabetes occurs when your blood glucose from the food you eat becomes too high. Insulin helps move glucose from our bloodstream into the body's cells to make energy but for some individuals, the pancreas does not make enough or use insulin well. (Learn about the different types here)",
    "There are 3 main types, type 1, type 2 and gestational diabetes, all being complex and serious.",
    "Type 1 diabetes is a chronic medical condition where cells that make insulin are destroyed, hence the body is unable to process glucose due to the lack of insulin. (Read more here)",
    "Type 2 diabetes is a chronic medical condition where your body is not able to respond to insulin as well as it should. In later stages, it also many not produce enough insulin. When uncontrolled, may lead to chronically high blood glucose levels, leading to serious complications. (Read more here)",
    "Gestational diabetes typically develops between the 24th to 28th week of pregnancy. Although not indicative of having diabetes before or after pregnancy, it raises the risk of type 2 diabetes in the future. If poorly managed, it can raise the child's chance of developing diabetes and create complications during pregnancy and delivery.",
];

const stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

const common_greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"];

const punctuation = /[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]/g;

function clean_tokens(text) {
    var tokens = text.toLowerCase().replace(punctuation, '').split(' ');
    tokens = tokens.filter(el => !stopwords.includes(el))
    return tokens
}

function check_keywords(text) {
    if (keywords.has(text)) {
        return info_map.get(keywords.get(text))
    } else {
        return false
    }
}

function respond(user_input) {

    user_input = user_input.toLowerCase();

    if (common_greetings.some(greeting => user_input.includes(greeting))) {
        return "Hello there, please ask a question!";
    } else if (keywords.has(user_input)) {
        return info_map.get(keywords.get(user_input));
    };
    // } else {
    //     var best_score = 0;
    //     let user_tokens = clean_tokens(user_input);

    //     info_list.forEach(info => {
    //         let info_tokens = clean_tokens(info);
    //         let info_score = info_tokens.filter(el => user_tokens.includes(el)).length

    //         if (info_score > best_score) {
    //             best_score = info_score
    //             answer = info
    //         }

    //     })
    // }

    return "Sorry I dont understand what you mean, please try again";
}

$(function () {
    $.backstretch("assets/img/bg.jpg");
    var count = 0;
    var classes = ["theme_1", "theme_2", "theme_3", "theme_4"];
    var length = classes.length;
    $(function () {
        $('.pvr_chat_wrapper').toggleClass('active');


        $('.pvr_chat_button, .pvr_chat_wrapper .close_chat').on('click', function () {
            $('.pvr_chat_wrapper').toggleClass('active');
            return false;
        });

        $('.message-input').on('keypress', function (e) {
            if (e.which == 13) {
                var val = ($(this).val() !== '') ? $(this).val() : "*empty frog croaks oh noe*";
                $('.chat-messages').append('<div class="message self"><div class="message-content">' + val + '</div></div>');
                $(this).val('');
                setTimeout(function () {
                    $('.chat-messages').append('<div class="message"><div class="message-content">' + respond(val) + '</div></div>');
                    $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                    $messages_w.perfectScrollbar('update');
                }, 200)
                var $messages_w = $('.pvr_chat_wrapper .chat-messages');
                $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                $messages_w.perfectScrollbar('update');
                return false;
            }
        });

        $('.pvr_chat_wrapper .chat-messages').perfectScrollbar();
        $(".change_chat_theme").on('click', function () {
            $(".chat-messages").removeAttr("class").addClass("chat-messages " + classes[count]);
            if (parseInt(count, 10) === parseInt(length, 10) - 1) {
                count = 0;
            } else {
                count = parseInt(count, 10) + 1;
            }
            var $messages_w = $('.pvr_chat_wrapper .chat-messages');
            $messages_w.scrollTop($messages_w.prop("scrollHeight"));
            $messages_w.perfectScrollbar('update');
        })
    });
});
