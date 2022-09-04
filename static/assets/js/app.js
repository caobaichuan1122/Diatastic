const info_list = [
    "Diabetes is a serious complex condition which can affect the entire body. Diabetes requires daily self care and if complications develop, diabetes can have a significant impact on quality of life and can reduce life expectancy. While there is currently no cure for diabetes, you can live an enjoyable life by learning about the condition and effectively managing it.",
    "There are main types of diabetes; all types are complex and serious. The three main types of diabetes are type 1, type 2 and gestational diabetes.",
    "When someone has diabetes, their body cannot maintain healthy levels of glucose in the blood. Glucose is a form of sugar which is the main source of energy for our bodies. Unhealthy levels of glucose in the blood can lead to long term and short term health complications. For our bodies to work properly we need to convert sugars from food into energy. Sugars from food are converted into glucose. A hormone called insulin is essential for the conversion of glucose into energy. In people with diabetes, insulin is no longer produced or not produced in sufficient amounts by the body. When people with diabetes eat foods that contain sugars or starches, such as breads, cereals, fruit and starchy vegetables and sweets, it cannot be converted into energy and the level of glucose in their blood rises and is harmful to them. Instead of being turned into energy the glucose stays in the blood resulting in high blood glucose levels. After eating, the glucose is carried around your body in your blood. Your blood glucose level is called glycaemia. Blood glucose levels can be monitored and managed through self care and treatment.",
    "Diabetes can be managed well but the potential complications are the same for type 1 and type 2 diabetes including heart attack, stroke, kidney disease, limb amputation, depression, anxiety and blindness. Early diagnosis, optimal treatment and effective ongoing support and management reduce the risk of diabetes-related complications.",
    "Type 2 diabetes is increasing at the fastest rate. There are large numbers of people with silent, undiagnosed type 2 diabetes which may be damaging their bodies. An estimated 2 million Australians are at high risk of developing type 2 diabetes and are already showing early signs of the condition. Type 2 diabetes is one of the major consequences of the obesity epidemic. The combination of massive changes to diet and the food supply, combined with massive changes to physical activity with more sedentary work and less activity, means most populations are seeing more type 2 diabetes. Genes also play a part with higher risk of type 2 diabetes in Chinese, South Asian, Indian, Pacific Islander and Aboriginal and Torres Strait Islander populations.",
    "In type 1 diabetes, symptoms are often sudden and can be life-threatening; therefore it is usually diagnosed quite quickly. In type 2 diabetes, many people have no symptoms at all, while other signs can go unnoticed being seen as part of getting older. Therefore, by the time symptoms are noticed, complications of diabetes may already be present. Common symptoms include: Being more thirsty than usual, passing more urine, feeling tired and lethargic, always feeling hungry, having cuts that heal slowly, itching, skin infections, blurred vision, unexplained weight loss (type 1), gradually putting on weight (type 2), mood swings, headaches, feeling dizzy, leg cramps"
];

const stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

const common_greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"];

const punctuation = /[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]/g;

function tokenize(text) {
    return text.replace(punctuation, '').split(' ');
}


function good_tokenize(text) {
    var tokens = tokenize(text);
    tokens = tokens.filter(el => !stopwords.includes(el))
    return tokens
}

function respond(user_input) {

    user_input = user_input.toLowerCase();

    var answer = "Sorry I dont understand what you mean, please try again";

    if (common_greetings.some(greeting => user_input.includes(greeting))) {
        answer = "Hello there, please ask a question!";
    } else {
        var best_score = 0;
        let user_tokens = good_tokenize(user_input);

        info_list.forEach(info => {
            let info_tokens = good_tokenize(info);
            let info_score = info_tokens.filter(el => user_tokens.includes(el)).length

            if (info_score > best_score) {
                best_score = info_score
                answer = info
            }

        })
    }

    return answer;
}

$(function () {
    $.backstretch("assets/img/bg.jpg");
    //www.bootstrapmb.com
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
                var val = ($(this).val() !== '') ? $(this).val() : "*empty frog croaks*";
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
        //www.bootstrapmb.com
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