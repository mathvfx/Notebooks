#ifndef KNearestNeighbor_Vector_hpp
#define KNearestNeighbor_Vector_hpp

#include <array>
#include <cmath>
#include <initializer_list>
#include <iostream>
#include <stdexcept>
#include <type_traits>

#include "Globals.hpp"

namespace MATH {

    /*
        This Vector class is a mathematics vector type which supports any
        finite dimensional vectors. Fundamental vector functions supporting
        any n-dimensions such as L2-norm, dot product, scalar-multiplications,
        etc. are provided. These are by no mean exhaustive for any general
        vector functions.
        
        Note that general multiplication and divison here are component-wise
        operation by convention.
     */
    template <size_t DIM, typename T=double>
    class Vector {
    public:
        Vector();
        Vector(T);
        Vector(std::initializer_list<T>);
        Vector(std::array<T, DIM>);
        Vector(const Vector& other); // Copy CTOR
        virtual ~Vector() = default;
        Vector& operator= (const Vector& other); // Copy-Assignment
        // Move-CTOR/Assignment not needed; we're not managing resources here.
    
        // General vector-valued functions
        size_t dim() const { return dimension; }
        T distance(const Vector&) const;
        T dot(const Vector&) const;  // a.k.a. Inner Product
        bool is_orthogonal(const Vector&) const;
        T norm() const;  // L2-Norm (a.k.a. length of vector)
        Vector normalize() const;
        T norm_squared() const;  // L2-Norm squared
        T scalar_projection(const Vector& from) const;
        Vector vector_projection(const Vector& from) const;
        
        // Vector equality
        bool operator== (const Vector&) const;
        bool operator!= (const Vector&) const;

        // Vector arithmetics
        Vector operator+ (const Vector&) const;
        Vector operator- (const Vector&) const;
        Vector& operator+= (const Vector&);
        Vector& operator-= (const Vector&);
        
        // Scalar multiplication
        Vector& operator*= (T);
        // Binary scalar multiplication overloaded globally.

        // Component-wise multiplication and division
        Vector operator* (const Vector&) const;
        Vector operator/ (const Vector&) const;
        Vector& operator/= (const Vector&);

        // Array-style component access
        T& operator[] (size_t idx); // Writable
        const T& operator[] (size_t idx) const; // Read-only
        
        // Negation (unary operator)
        Vector operator- () const;

    private:
        T arr[DIM];  // Storage for a vector
        size_t dimension {DIM}; // Dimension of a vector
    }; // END class Vector

} // END namespace MATH


//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
// Class Definitions


// Rule of Big Three

template <size_t DIM, typename T> // Default CTOR
MATH::Vector<DIM,T>::Vector() {
    static_assert(DIM > 0, "Dimension must be at least 1");
    static_assert(std::is_arithmetic<T>(), "<T> must be numerics");
}


template <size_t DIM, typename T> // Uniform vector CTOR
MATH::Vector<DIM,T>::Vector(T v) {
    static_assert(DIM > 0, "Dimension must be at least 1");
    static_assert(std::is_arithmetic<T>(), "<T> must be numerics");
    for (size_t i{}; i < DIM; ++i)
        arr[i] = v;
}


template <size_t DIM, typename T> // Parameterized CTOR
MATH::Vector<DIM,T>::Vector(std::initializer_list<T> lst) {
    static_assert(DIM > 0, "Dimension must be at least 1");
    static_assert(std::is_arithmetic<T>(), "<T> must be numerics");
    for (size_t i{}; i < lst.size() && i < DIM; ++i)
        arr[i] = *(lst.begin()+i);
}


template <size_t DIM, typename T> // Parameterized CTOR
MATH::Vector<DIM,T>::Vector(std::array<T,DIM> arr_list) {
    static_assert(DIM > 0, "Dimension must be at least 1");
    static_assert(std::is_arithmetic<T>(), "<T> must be numerics");
    for (size_t i{}; i < DIM; ++i)
        arr[i] = *(arr_list.begin()+i);
}


template <size_t DIM, typename T> // Copy CTOR
MATH::Vector<DIM,T>::Vector(const Vector& other)
    : dimension{other.dimension} {
    static_assert(DIM > 0, "Dimension must be at least 1");
    static_assert(std::is_arithmetic<T>(), "<T> must be numerics");
    for (size_t i{}; i < dimension; ++i)
        arr[i] = other.arr[i];
}


template <size_t DIM, typename T> // Copy-Assignment
MATH::Vector<DIM,T>& MATH::Vector<DIM,T>::operator= (const Vector& other) {
    if (this == &other) return *this;
    dimension = other.dimension;
    for (size_t i{}; i < dimension; ++i)
        arr[i] = other.arr[i];
    return *this;
}


// Elementary Vector Functions


template <size_t DIM, typename T>
T MATH::Vector<DIM,T>::distance(const Vector& other) const {
    return (*this - other).norm();
}


template <size_t DIM, typename T>
T MATH::Vector<DIM,T>::dot(const Vector& other) const {
    T sum {};
    for (size_t i{}; i < DIM; ++i)
        sum += arr[i] * other[i];
    return sum;
}


template <size_t DIM, typename T>
bool MATH::Vector<DIM,T>::is_orthogonal(const Vector& other) const {
    return 0 == this->dot(other);
}


template <size_t DIM, typename T>
T MATH::Vector<DIM,T>::norm() const {
    T sum {};
    for (size_t i{}; i < DIM; ++i)
        sum += arr[i] * arr[i];
    return std::sqrt(sum);
}


template <size_t DIM, typename T>
MATH::Vector<DIM,T> MATH::Vector<DIM,T>::normalize() const {
    auto divisor = this->norm();
    if (KNN::FpEquality<T>(0, divisor))
        return *this; // returning zero vector as it is
    return *this/divisor;
}


template <size_t DIM, typename T>
T MATH::Vector<DIM,T>::norm_squared() const {
    T sum {};
    for (size_t i{}; i < DIM; ++i)
        sum += arr[i] * arr[i];
    return sum;
}


template <size_t DIM, typename T>
T MATH::Vector<DIM,T>::scalar_projection(const Vector& from) const {
    auto divisor = this->norm_squared();
    if (KNN::FpEquality<T>(0, divisor))
        return 0; // projection of zero vector is defined as zero.
    return this->dot(from) / std::sqrt(divisor);
}


template <size_t DIM, typename T>
MATH::Vector<DIM,T> MATH::Vector<DIM,T>::vector_projection(const Vector& from) const {
    auto divisor = this->norm_squared();
    if (KNN::FpEquality<T>(0, divisor))
        return *this; // return zero vector as it is.
    return *this * this->dot(from) / divisor;
}


// Method Operator-Overload


template <size_t DIM, typename T>
T& MATH::Vector<DIM,T>::operator[] (size_t idx) {
    if (idx >= DIM)
        throw std::out_of_range {"Attempt to write out of bound."};
    return arr[idx];
}


template <size_t DIM, typename T>
const T& MATH::Vector<DIM,T>::operator[] (size_t idx) const {
    if (idx >= DIM)
        throw std::out_of_range {"Attempt to read out of bound."};
    return arr[idx];
}


template <size_t DIM, typename T>
bool MATH::Vector<DIM,T>::operator== (const Vector& other) const {
    for (size_t i{}; i < DIM; ++i)
        if (!KNN::FpEquality(arr[i], other.arr[i]))
            return false;
    return true;
}


template <size_t DIM, typename T>
bool MATH::Vector<DIM,T>::operator!= (const Vector& other) const {
    return !(*this == other);
}


template <size_t DIM, typename T>
MATH::Vector<DIM,T>& MATH::Vector<DIM,T>::operator*= (T val) {
    for (size_t i{}; i < DIM; ++i)
        arr[i] *= val;
    return *this;
}


template <size_t DIM, typename T> // Component-wise multiplication
MATH::Vector<DIM,T> MATH::Vector<DIM,T>::operator* (const Vector& v) const {
    Vector<DIM,T> vec {*this};
    for (size_t i{}; i < DIM; ++i)
        vec[i] *= v[i];
    return std::move(vec);
}


template <size_t DIM, typename T> // Component-wise division
MATH::Vector<DIM,T> MATH::Vector<DIM,T>::operator/ (const Vector& v) const {
    Vector<DIM,T> vec {*this};
    for (size_t i{}; i < DIM; ++i)
        vec[i] /= v[i];
    return std::move(vec);
}


template <size_t DIM, typename T> // Component-wise division-assignment
MATH::Vector<DIM,T>& MATH::Vector<DIM,T>::operator/= (const Vector& v) {
    for (size_t i{}; i < DIM; ++i)
        arr[i] /= v[i];
    return *this;
}


template <size_t DIM, typename T>
MATH::Vector<DIM,T> MATH::Vector<DIM,T>::operator+ (const Vector& v) const {
    Vector<DIM,T> vec {*this};
    for (size_t i{}; i < DIM; ++i)
        vec[i] += v[i];
    return std::move(vec);
}


template <size_t DIM, typename T>
MATH::Vector<DIM,T>& MATH::Vector<DIM,T>::operator+= (const Vector& v) {
    for (size_t i{}; i < DIM; ++i)
        arr[i] += v[i];
    return *this;
}


template <size_t DIM, typename T>
MATH::Vector<DIM,T> MATH::Vector<DIM,T>::operator- (const Vector& v) const {
    Vector<DIM,T> vec {*this};
    for (size_t i{}; i < DIM; ++i)
        vec[i] -= v[i];
    return std::move(vec);
}


template <size_t DIM, typename T> // Unary operator: Negation
MATH::Vector<DIM,T> MATH::Vector<DIM,T>::operator- () const {
    return (*this * -1);
}


template <size_t DIM, typename T>
MATH::Vector<DIM,T>& MATH::Vector<DIM,T>::operator-= (const Vector& v) {
    for (size_t i{}; i < DIM; ++i)
        arr[i] -= v[i];
    return *this;
}


// Global Operator-Overload


template <size_t DIM, typename T, typename U> // LHS scalar multiply
MATH::Vector<DIM,T> operator* (U val, const MATH::Vector<DIM,T>& v) {
    MATH::Vector<DIM,T> vec;
    for (size_t i{}; i < DIM; ++i)
        vec[i] = v[i] * val;
    return std::move(vec);
}


template <size_t DIM, typename T, typename U> // RHS scalar multiply
MATH::Vector<DIM,T> operator* (const MATH::Vector<DIM,T>& v, U val) {
    MATH::Vector<DIM,T> vec;
    for (size_t i{}; i < DIM; ++i)
        vec[i] = v[i] * val;
    return std::move(vec);
}


template <size_t DIM, typename T, typename U> // LHS scalar addition
MATH::Vector<DIM,T> operator+ (U val, const MATH::Vector<DIM,T>& v) {
    MATH::Vector<DIM,T> vec {v};
    for (size_t i{}; i < DIM; ++i)
        vec[i] += val;
    return std::move(vec);
}


template <size_t DIM, typename T, typename U> // RHS scalar addition
MATH::Vector<DIM,T> operator+ (const MATH::Vector<DIM,T>& v, U val) {
    MATH::Vector<DIM,T> vec {v};
    for (size_t i{}; i < DIM; ++i)
        vec[i] += val;
    return std::move(vec);
}


template <size_t DIM, typename T, typename U> // LHS scalar subtraction
MATH::Vector<DIM,T> operator- (U val, const MATH::Vector<DIM,T>& v) {
    MATH::Vector<DIM,T> vec;
    for (size_t i{}; i < DIM; ++i)
        vec[i] = val - v[i];
    return std::move(vec);
}


template <size_t DIM, typename T, typename U> // RHS scalar subtraction
MATH::Vector<DIM,T> operator- (const MATH::Vector<DIM,T>& v, U val) {
    MATH::Vector<DIM,T> vec {v};
    for (size_t i{}; i < DIM; ++i)
        vec[i] -= val;
    return std::move(vec);
}


template <size_t DIM, typename T>
inline std::ostream& operator<< (std::ostream& os, const MATH::Vector<DIM,T>& v) {
    if (&os == &std::cout) {
        os << "[";
        for (size_t i{}; i < DIM-1; ++i)
            os << v[i] << ", ";
        os << v[DIM-1] << "]";
    } else
        for (size_t i{}; i < DIM; ++i)
            os << v[i] << " ";
    return os;
}

#endif /* KNearestNeighbor_Vector_hpp */
