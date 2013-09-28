---
layout : post
tags : [C++, C++11]
category :
- C-Cpp
---
{% include JB/setup %}

零星看了一些C++11的新特性，又在面试过程中被问道一些跟C++11新特性有关的内容，所以就写点东西总结一下吧，这篇文章先写写C++11中那些新的关键字（也包括语义发生了变化的）

###类相关
final 和 override
在C++03中，如果要实现一个不能继承的类，我们或许需要通过一些不是很直观的设计来达到目的：
<pre>
<code class="cpp">
    template<class T>
    class NoInheritBase{
    friend T; 
    private:
        NoInheritBase(){}
        ~NoInheritBase(){}
    };
    class NoInherit:public NoInheritBase<NoInherit>{
        //members and function members;
    };
    class ErrorInherit:public NoInherit{}; //错误
</code>
</pre>

这种设计的思想是将类(NoInheritBase)的构造函数和析构函数设置为私有函数，同时为了解决类本身无法构造的问题，通过子类(NoInherit)对其继承并将子类设置为父类的友元函数,这样所有继承NoInherit类的子类都需要调用NoInheritBase的构造函数,但是由于NoInheritBase的构造函数是私有的,而且只有NoInherit一个友元函数,所以所有继承自NoInherit的类都会产生一个编译错误。
再看另外一个场景，在一个层次化的多个类之间，如果想将一个子类的virtual函数设置为最终实现，即不允许子类再重写，这时候上面的方法就爱莫能助了。

在C++11中，引入了final关键字，使用final来解决上面两个问题都是非常简单且直观的。

<pre>
<code class="cpp">
    class NoInheritSimple final{};
    class ErrorInherit_1:public NoInheritSimple{}; //error
    class Base{
        virtual void dummy() final{} //final function
    };
    class Inherit: public Base{
        virtual void dummy() {/*function body*/ } // error, can not override final function
    };
</code>
</pre>

