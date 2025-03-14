[Specifications](../specifications.md) > [Software Architecture](../specifications.md#software-architecture) > Components

---

# Components

In an early development phase, I decided to deliver *novelibre* as a component, 
i.e. in the form of a single Python module. 
This component should include everything necessary that is not provided by the 
Windows Python installation. 

An alternative would have been to deliver the fully modularized program, as is
structured for development, with its class libraries packaged, e.g. via PyPi. 
I decided against this, on the one hand to avoid the issues of version dependency, 
and on the other to be able to freely design the plugin system as mentioned below. 
So far this has worked well.

In order to keep the program reasonably lean, functions that not everyone needs 
should be installed separately as additional components, so-called plugins.
These plugins have almost unlimited access to the entire functionality of 
*novelibre*, which means they are extremely tightly coupled, which represents 
a certain risk, but also allows powerful features.  


![UML Component diagram](_images/novelibre_components.png)

