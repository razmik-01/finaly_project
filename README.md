# final_project
Final project structure


Պրոյեկտը նման է լինելու առևտրային վեբ կայքի, որտեղ user-ը կարող է ընտրել ապրանքներ՝ գնումներ կատարելու համար,
կարող է գրանցվել կցել քարտ, կլինի նաև չատ խնդիրներ արագ լուծման համար։

բաղկացաց է լինելու հետևյալ էջերից(ֆունկցիոնալություն)՝

    landing page(գլխավոր էջ, որտեղ կլինի մի քանի ապրանքներ,որոնք կարող է պատվիրել) 
    login, registration(որպեսզի կարողանա օգտատերը պատվերվեր իրականացնի)    
    personal page(որպեսզի օգտատերը կարողանալ փոխել իր էջի login password-ը, կցել քարտ)
    contact us page(օգտատերը կկարողանա կապ հաստատաել ընկերության հետ։Նաև օնլայն չատի հնարավորություն)
    payment page(վճարումներ կատարելու համար)
    cart page(օգտատերը կարող է ցանկացաց ապրանք պահպանել զամբյուղում, միանգամից վճարելու համար    



django structure 


Django Models

    User
    Product
    Cart
    Order
    Payment
    Chat


User model-ը Cart մոդելի հետ, տարբեր օգտատերները 1 զամբյուղի,
Product-ը Cart մոդելի հետ, տարբեր պրոդուկները մեկ զամբյուղի հետ,
Order-ը User-ի հետ, տարբեր վճարումներ մեկ օգտատիրոջ հետ,
Payment-ը Cart-ի հետ.


View Functions

    landing_page
    login/registration
    personal_page
    contact_us
    payment_page
    cart

