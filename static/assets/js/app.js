const keywords = {
    "what is diabetes": 0,
    "type": 1,
    "types": 2,
    "type1": 2,
    "type2": 3,
    "type 1": 2,
    "type 2": 3,
    "gestational": 4,
    "hypoglycemia": 5,
    "symptoms": 6,
    "?help": 7,
    "?diet": 8,
    "?treament": 9,
    "syndrome": 10,
    "long term": 11,
    "treatment": 12,
    "diet": 13,
    "eat": 13,
    "eating": 13,
    "foods": 13,
    "food": 13,
    "daily": 14,
    "routine": 14,
    "look": 15,
    "look after": 15,
    "monitor": 15,
    "habits": 15,
    "habit": 15,
    "?diary": 16
};


const responses = {
    0: "Diabetes occurs when your blood glucose from the food you eat becomes too high. Insulin helps move glucose from our bloodstream into the body's cells to make energy but for some individuals, the pancreas does not make enough or use insulin well.",
    1: "There are 3 main types, type 1, type 2 and gestational diabetes, all being complex and serious.",
    2: "Type 1 diabetes is a chronic medical condition where cells that make insulin are destroyed, hence the body is unable to process glucose due to the lack of insulin.",
    3: "Type 2 diabetes is a chronic medical condition where your body is not able to respond to insulin as well as it should. In later stages, it also many not produce enough insulin. When uncontrolled, may lead to chronically high blood glucose levels, leading to serious complications.",
    4: "Gestational diabetes typically develops between the 24th to 28th week of pregnancy. Although not indicative of having diabetes before or after pregnancy, it raises the risk of type 2 diabetes in the future. If poorly managed, it can raise the child's chance of developing diabetes and create complications during pregnancy and delivery.",
    5: "Hypoglycemia happens when blood glucose falls low, possibly a side effect of insulin. Severely low blood glucose can cause serious complications, including passing out, coma, or death. Symptoms include rapid heartbeat, sweating, confusion, slurred speech, numbness in fingers, toes and lips",
    6: "Being thirsty, needing to pee, always feeling hungry, itching, losing weight",
    7: "Available commands: ?diet, ?treatment",
    8: "//Healthy eating is essential etc. REDIRECTING YOU TO THE GUIDE//",
    9: "//Explore your treatment options here, includes all types of diabetes. REDIRECTING YOU TO THE GUIDE//",
    10: "HHNS is when your blood glucose level goes way too high, and if you don’t treat it, it can cause death.",
    11: "Likely to develop heart disease, nerve damage (diabetic neuropathy), kidney damage, diabetic eye disease",
    12: "Type 1: Insulin, Type 2: Diabetic pills and/or non-insulin injectables",
    13: "Yes: Fruits, veges, legummes, poultry, avocados, nuts, seeds. No: Sugar, candy, soda, hot dogs, fatty red meat, butter",
    14: "Check blood sugar 3-4 times a day, avoid skipping meals, exercise more, get enough sleep",
    15: "Test blood glucose levels regularly, take insulin, stay active, have a healthy eating plan",
    16: "//REDIRECTING YOU TO THE DIARY PAGE//"
};

const stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

const common_greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"];

const punctuation = /[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]/g;

function clean_tokens(text) {
    var tokens = text.toLowerCase().replace(punctuation, '').split(' ');
    return tokens.filter(el => !stopwords.includes(el))
}

function check_keywords(text) {
    if (keywords.has(text)) {
        return responses.get(keywords.get(text))
    }
    return false
}

function respond(user_input) {

    user_input = user_input.toLowerCase();

    if (common_greetings.some(greeting => user_input.includes(greeting))) {
        return "Hello there, please ask a question!";
    }

    if (user_input in keywords) {
        switch (keywords[user_input]) {
            case 8:
                window.location.href = "../guide"
                break;
            case 9:
                window.location.href = "../guide"
                break;
            case 16:
                window.location.href = "../diary"
        };
        return responses[keywords[user_input]];
    }

    return "Sorry I dont understand what you mean, please try again";
}

$(function () {
    $.backstretch("assets/img/bg.jpg");
    $(function () {
        $('.pvr_chat_wrapper').toggleClass('active');


        $('.pvr_chat_button, .pvr_chat_wrapper .close_chat').on('click', function () {
            $('.pvr_chat_wrapper').toggleClass('active');
            return false;
        });

        $('.message-input').on('keypress', function (e) {
            if (e.which == 13) {
                if ($(this).val() == '') {
                    return False
                }
                var val = $(this).val();

                $('.chat-messages').append(`<div class="message self"><div class="message-content">${val}</div></div>`);

                $(this).val('');

                setTimeout(function () {
                    $('.chat-messages').append(`<div class="message"><div class="message-content">${respond(val)}</div></div>`);
                    $messages_w.scrollTop($messages_w.prop("scrollHeight"));
                    $messages_w.perfectScrollbar('update');
                }, 200)

                var $messages_w = $('.pvr_chat_wrapper .chat-messages');
            }
        });

        $('.pvr_chat_wrapper .chat-messages').perfectScrollbar();
    });
});