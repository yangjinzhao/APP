$(function () {

    $(".confirm").click(function () {
        var $confirm = $(this)

        var $li = $confirm.parents('li')

        var cartid = $li.attr('cartid')
        //
        $.getJSON('/app/changecartstate/', {"cartid": cartid}, function (data) {
            console.log(data)
            if (data.status == 'ok') {
                if (data.is_select) {
                    $confirm.find('span').find('span').html('√')
                } else {
                    $confirm.find('span').find('span').html("")
                }

                //改总价
                $('#totalprice').text(data.total_price)
            }
        })

    })

    // 减少的时候
    $(".subShopping").change(function () {
        var $subShopping = $(this)
        var $li = $subShopping.parents('li')
        var cartid = $li.attr('cartid')

        //发送ajax请求
        $.getJSON('/app/subshopping/', {'cartid': cartid}, function (data) {
            console.log(data)
            if (data.status == 'ok') {
                //改总价
                $('#totalprice').text(data.total_price)
                if (data.cart_goods_num > 0) {
                    $subShopping.next('span').text(data.cart_goods_num)
                } else {
                    $li.remove()
                }

            }
        })
    })


    // 添加商品
       $(".addShopping").click(function () {
        var $addShopping = $(this)
        var $li = $addShopping.parents('li')
        var cartid = $li.attr('cartid')

        $.getJSON('/app/addshopping/', {'cartid': cartid}, function (data) {
            console.log(data)
            if (data.status == 'ok') {
                //改总价
                $('#totalprice').text(data.total_price)
                $addShopping.prev('span').text(data.cart_goods_num)
            }
        })
    })


   $(".all_select").click(function () {
        var $allselect = $(this)
        var $span = $allselect.find('span').find('span')
        var content = $span.html()
        if (content == '') {
            // 即将要做全选
            $.getJSON('/app/allselect/', {}, function (data) {
                console.log(data)
                if (data.status == 'ok') {
                    //改总价
                    $('#totalprice').text(data.total_price)
                    $allselect.find('span').find('span').html('√')
                    $(".confirm").find('span').find('span').html("√")
                }
            })
        } else if(content == '√') {
            //即将要做取消
            $.getJSON('/app/unallselect/', {}, function (data) {
                console.log(data)
                if (data.status == 'ok') {
                    //改总价
                    $('#totalprice').text(data.total_price)
                    $allselect.find('span').find('span').html('')
                    $(".confirm").find('span').find('span').html("")
                }
            })
        }


    })

    $("#make_order").click(function () {

        var select_list = [];

        var unselect_list = [];

        $(".confirm").each(function () {

            var $confirm = $(this);

            var cartid = $confirm.parents("li").attr("cartid");

            if ($confirm.find("span").find("span").html().trim()) {
                select_list.push(cartid);
            } else {
                unselect_list.push(cartid);
            }

        })

        if (select_list.length === 0) {
            return
        }

        $.getJSON("/axf/makeorder/", function (data) {
            console.log(data);

            if (data['status'] === 200) {
                window.open('/axf/orderdetail/?orderid=' + data['order_id'], target = "_self");
            }

        })
    })


})