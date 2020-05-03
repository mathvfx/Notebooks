#include <chrono>
#include <cmath>
#include <iostream>
#include <iomanip>
#include <random>
#include <stdexcept>
#include <utility>
#include <vector>
#include "gtest/gtest.h"

#include "Globals.hpp"
#include "BoundedVector.hpp"
#include "CompleteBinaryTree.hpp"
#include "NearestNeighbor.hpp"
#include "Vector.hpp"
#include "WavefrontObject.hpp"

using std::cout;
using std::boolalpha;
using std::endl;
using std::setprecision;

// Note the use of namespace here is purely for sectioning and organization

namespace Test_MathVector {
    struct Fixture_MathVector : ::testing::Test {
        using Real = double;
        MATH::Vector<5, Real> vec_1 {10, 20, 30, 40, 50};
        MATH::Vector<5, Real> vec_2 {100000.002, 20, 0.0000002, 4.000005, 10};
        MATH::Vector<4, Real> vec_a {-1, 5, 2, -3};
        MATH::Vector<4, Real> vec_b {2, 0.75, 2, -2};
        MATH::Vector<3, Real> vec_c {-1, 5, 2};
        MATH::Vector<3, Real> vec_d {2, 0.75, 2};
        MATH::Vector<3, Real> vec_e {2, 2, -1};
        MATH::Vector<3, Real> vec_f {5, -4, 2};
    };
    TEST_F(Fixture_MathVector, CTOR_From_Uniform_Scalar) {
        // Can construct vector from a single scalar
        Real init = 100.1;
        MATH::Vector<5, Real> vec_10 (init);
        ASSERT_EQ(5, vec_10.dim());
        for (size_t i{}; i < vec_10.dim(); ++i)
            ASSERT_EQ(init, vec_10[i]);
    }
    TEST_F(Fixture_MathVector, CTOR_From_InitializationList) {
        auto my_list = std::initializer_list<Real>({100, 200, 300, 400, 500});
        
        // Can initialize a smaller vector than initializer list
        MATH::Vector<3, Real> vec_10 {my_list};
        for (size_t i{}; i < vec_10.dim(); ++i)
            ASSERT_TRUE(KNN::FpEquality<Real>(*(my_list.begin()+i), vec_10[i]));

        // Can initialize a larger vector than initializer list
        MATH::Vector<7, Real> vec_11 {my_list};
        for (size_t i{}; i < my_list.size(); ++i)
            ASSERT_TRUE(KNN::FpEquality<Real>(*(my_list.begin()+i), vec_11[i]));
        for (size_t i {my_list.size()}; i < vec_11.dim(); ++i)
            ASSERT_TRUE(KNN::FpEquality<Real>(0, vec_11[i]));
            
        // Can handle default construction
        MATH::Vector<5, Real> vec_12 {};
        for (size_t i{}; i < vec_12.dim(); ++i)
            ASSERT_TRUE(KNN::FpEquality<Real>(0, vec_12[i]));
    }
    TEST_F(Fixture_MathVector, Copy_Construction) {
        auto vec_cp {vec_1};
        
        // Copy has same elements and dimension
        for (size_t i{}; i < vec_1.dim(); ++i)
            ASSERT_TRUE(KNN::FpEquality<Real>(vec_cp[i], vec_1[i]));
        ASSERT_EQ(vec_cp.dim(), vec_1.dim());
        
        // Can copy-assign
        MATH::Vector<5, Real> vec_cp_assign {};
        vec_cp_assign = vec_1;
        for (size_t i{}; i < vec_1.dim(); ++i)
            ASSERT_TRUE(KNN::FpEquality<Real>(vec_cp_assign[i], vec_1[i]));
        ASSERT_EQ(vec_cp_assign.dim(), vec_1.dim());
    }
    TEST_F(Fixture_MathVector, Using_Array_Indices_Style) {
        auto vec_10 {vec_1};
        
        // Can access vector component using array-style indices
        for (size_t i{}; i < vec_10.dim(); ++i)
            ASSERT_TRUE(KNN::FpEquality(vec_10[i], vec_1[i]));
            
        // Can write to vector via array-style indices
        for (size_t i{}; i < vec_10.dim(); ++i) {
            vec_10[i] = vec_1[i] * 2;
            ASSERT_TRUE(KNN::FpEquality(vec_10[i], vec_1[i]*2));
        }
        
        // Will throw when accessing (or writing) out-of-bound
        ASSERT_THROW(vec_10[vec_10.dim() + 1], std::out_of_range);
    }
    TEST_F(Fixture_MathVector, Arithmetic_Operations) {
        auto vec_10 {vec_1};
        
        // Can chain addition
        ASSERT_NO_THROW(vec_1 + vec_10 + vec_1);
        ASSERT_NO_THROW(100 + vec_10 + 150.0);

        // Can chain subtractiion
        ASSERT_NO_THROW(vec_1 - vec_10 - vec_1);
        ASSERT_NO_THROW(5 - vec_10 - 7 - vec_10);
                
        // Can chain scalar multiply (both at LHS and RHS scalar)
        ASSERT_NO_THROW(1.5 * vec_10 * 2);
        
        // Can chain component-multiply
        ASSERT_NO_THROW(vec_10 * vec_10 * vec_10);
        
        // Can chain component-divide
        ASSERT_NO_THROW(vec_10/vec_10/vec_10);
        MATH::Vector<5, Real> ones(1);
        ASSERT_TRUE((vec_10/vec_10) == ones);
        
        // Can assert vector equality
        auto vec_11 {vec_1 * vec_1};
        auto vec_12 {10 * vec_1};
        MATH::Vector<5, Real> vec_13 {100, 400, 900, 1600, 2500};
        ASSERT_TRUE(vec_11 != vec_12);
        ASSERT_TRUE(vec_11 == vec_13);

        // Can apply +=, -=, *=, and /=
        auto vec_20 = vec_1; // Copy-CTOR
        vec_20 *= 10;
        EXPECT_TRUE(vec_20 == vec_12);
        auto vec_21 = vec_1;
        vec_21 -= 0.31415;
        MATH::Vector<5, Real> vec_21_verify
            {9.68585, 19.68585, 29.68585, 39.68585, 49.68585 };
        for (size_t i{}; i < 5; ++i)
            EXPECT_TRUE(KNN::FpEquality(vec_21[i], vec_21_verify[i]));
        EXPECT_TRUE(vec_21 == vec_21_verify);
        vec_21 += 0.31415;
        EXPECT_TRUE(vec_21 == vec_1);
        
        vec_21 /= vec_1;
        EXPECT_TRUE(vec_21 == ones);
        
        // Can negate
        vec_21 = vec_1;
        vec_21 *= -1;
        EXPECT_TRUE(vec_21 == -vec_1);
    }
    TEST_F(Fixture_MathVector, Elementary_Vector_Operations) {
        EXPECT_EQ(5.75, vec_c.dot(vec_d));
        EXPECT_TRUE(KNN::FpEquality<Real>(5.75, vec_d.dot(vec_c)));
        EXPECT_TRUE(KNN::FpEquality<Real>(11.75, vec_a.dot(vec_b)));
        EXPECT_EQ(39, vec_a.norm_squared());
        ASSERT_TRUE(KNN::FpEquality<Real>(6.244997, vec_a.norm(), 1e-6));
        
        MATH::Vector<4, Real> zero {};
        ASSERT_TRUE(zero == zero.normalize());

        MATH::Vector<4, Real> vec_a_unit_verify =
                            { static_cast<Real>(-1.0/std::sqrt(39.0)),
                              static_cast<Real>(5.0/std::sqrt(39.0)),
                              static_cast<Real>(2.0/std::sqrt(39.0)),
                              static_cast<Real>(-3.0/std::sqrt(39.0)) };
        EXPECT_TRUE(vec_a_unit_verify == vec_a.normalize());
        ASSERT_TRUE(vec_e.is_orthogonal(vec_f));

        MATH::Vector<3, Real> va {-2,3,1};
        MATH::Vector<3, Real> vb {1,1,2};
        auto comp_proj_of_vb_onto_va = va.scalar_projection(vb);
        EXPECT_TRUE(KNN::FpEquality<Real>(3.0/std::sqrt(14), comp_proj_of_vb_onto_va));
        auto vec_proj_of_vb_onto_va = va.vector_projection(vb);
        MATH::Vector<3, Real> vb_proj_verify {-3.0/7.0, 9.0/14.0, 3.0/14.0};
        EXPECT_TRUE(vec_proj_of_vb_onto_va == vb_proj_verify);
    }
} // END namespace Test_MathVector

namespace Test_WavefrontObject {
    TEST(Test_WavefrontObject, Exception_On_Nonexistence_File) {
        ASSERT_THROW(KNN::WavefrontObject my_bad_file {R"(./data/NOTHING.abc)"},
                     std::exception);
    }
    TEST(Test_WavefrontObject, Exception_On_Non_File) {
        ASSERT_THROW(KNN::WavefrontObject my_bad_file {R"(./data)"},
                     std::exception);
    }
    TEST(Test_WavefrontObject, Loading_Empty_Wavefront_Obj_File) {
        KNN::WavefrontObject my_empty_file {R"(./data/this_is_empty.obj)"};
        EXPECT_TRUE(my_empty_file.is_loaded());
        ASSERT_TRUE(my_empty_file.is_empty());
        ASSERT_EQ(0, my_empty_file.get_point_count());
    }
    TEST(Test_WavefrontObject, Loading_File__grid_ptcld_10) {
        KNN::WavefrontObject my_file {R"(./data/grid_ptcld_10.obj)"};
        EXPECT_TRUE(my_file.is_loaded());
        ASSERT_FALSE(my_file.is_empty());
        ASSERT_EQ(10, my_file.get_point_count());
        
        MATH::Vector<KNN::DIMENSION, KNN::PRECISION> point3
            {-2.51144075, 0, 1.14180732};
        ASSERT_TRUE(point3 == my_file[3]);
        ASSERT_FALSE(point3 == my_file[4]);
        ASSERT_THROW(my_file[3000000], std::out_of_range);
        
        MATH::Vector<KNN::DIMENSION, KNN::PRECISION> min_bound
            {-4.79356575, 0, -4.92551804};
        EXPECT_TRUE(min_bound == my_file.get_min_bound());
        MATH::Vector<KNN::DIMENSION, KNN::PRECISION> max_bound
            {3.37521338, 0, 2.56993532};
        EXPECT_TRUE(max_bound == my_file.get_max_bound());
    }
} // END namespace Test_WavefrontObject

namespace Test_CompleteBinaryTree {
    struct Fixture_CompleteBinaryTree : ::testing::Test {
        constexpr static size_t ELEM_SIZE = 10; // Please use value >= 10
        // KNN::MathVector3 is an alias found in CompleteBinaryTree.hpp
        std::vector<KNN::MathVector> mock_point_list;
        KNN::CompleteBinaryTree my_CBT_list {ELEM_SIZE};
        
        // Constructor
        Fixture_CompleteBinaryTree() {
            // Mock WavefrontObject::point_list
            for (int i{}; i < ELEM_SIZE; ++i)
                mock_point_list.emplace_back(KNN::MathVector(i*11));
                
            // Mock CompleteBinaryTree::cbt_pod_list
            my_CBT_list.build_breath_first(mock_point_list);
        } // END constructor Fixture_CompleteBinaryTree
    };
    TEST_F(Fixture_CompleteBinaryTree, Verify_Rule_Of_Big_Five) {
        // Parameterized CTOR was tested in Fixture_CompleteBinaryTree class
        
        // Verify copy CTOR
        KNN::CompleteBinaryTree copy_ctor_list = my_CBT_list;
        ASSERT_NE(&copy_ctor_list, &my_CBT_list);
        for (size_t i{}; i < ELEM_SIZE; ++i) {
            // verify copy-CTOR ptcoord and original point_list has same addr.
            ASSERT_EQ(copy_ctor_list[i].ptcoord, my_CBT_list[i].ptcoord);
            ASSERT_EQ(copy_ctor_list[i].ptcoord, &mock_point_list[i]);
        }
        // Verify move CTOR
        ASSERT_EQ(ELEM_SIZE, copy_ctor_list.size());
        KNN::CompleteBinaryTree move_ctor_list = std::move(copy_ctor_list);
        ASSERT_EQ(0, copy_ctor_list.size());
        for (size_t i{}; i < ELEM_SIZE; ++i)
            ASSERT_EQ(move_ctor_list[i].ptcoord, &mock_point_list[i]);
            
        // Verify copy assignment
        copy_ctor_list = my_CBT_list; // copy assign
        ASSERT_EQ(ELEM_SIZE, copy_ctor_list.size());
        for (size_t i{}; i < ELEM_SIZE; ++i)
            ASSERT_EQ(copy_ctor_list[i].ptcoord, &mock_point_list[i]);

        // Verify move assignment
        KNN::CompleteBinaryTree move_assign_list;
        ASSERT_EQ(0, move_assign_list.size());
        move_assign_list = std::move(copy_ctor_list); // move assign
        ASSERT_EQ(0, copy_ctor_list.size());
        ASSERT_EQ(ELEM_SIZE, move_assign_list.size());
        for (size_t i{}; i < ELEM_SIZE; ++i)
            ASSERT_EQ(move_assign_list[i].ptcoord, &mock_point_list[i]);
    }
    TEST_F(Fixture_CompleteBinaryTree, Verify_Pointer_To_PointList_Addresses) {
        // Verify correct element size
        ASSERT_EQ(ELEM_SIZE, my_CBT_list.size());
        ASSERT_EQ(ELEM_SIZE, mock_point_list.size());

        // Verify memory addresses
        for (size_t i{}; i < ELEM_SIZE; ++i) {
            ASSERT_EQ(my_CBT_list[i].ptcoord, &mock_point_list[i]); // Addresses
            ASSERT_EQ(*my_CBT_list[i].ptcoord, mock_point_list[i]);   // Elements
        }
        
        // Verify that mutating my_list will affect mock_point_list
        *my_CBT_list[ELEM_SIZE-7].ptcoord = {3000, 300, 30};
        ASSERT_EQ(*my_CBT_list[3].ptcoord, mock_point_list[3]);
        
        // Verify that mutating mock_point_list will affect my_list
        mock_point_list[ELEM_SIZE-3] = {-7, 70, 700};
        ASSERT_EQ(*my_CBT_list[7].ptcoord, mock_point_list[7]);

        // Verify parent address matches list address (a few samples)
        ASSERT_EQ(my_CBT_list.parent(0).ptcoord, &mock_point_list[0]);
        ASSERT_EQ(my_CBT_list.parent(2).ptcoord, &mock_point_list[0]);
        ASSERT_EQ(my_CBT_list.parent(3).ptcoord, &mock_point_list[1]);
        ASSERT_EQ(my_CBT_list.parent(9).ptcoord, &mock_point_list[4]);

        // Verify left-child address matches list address (a few samples)
        ASSERT_EQ(my_CBT_list.left_child(0).ptcoord, &mock_point_list[1]);
        ASSERT_EQ(my_CBT_list.left_child(2).ptcoord, &mock_point_list[5]);
        ASSERT_EQ(my_CBT_list.left_child(3).ptcoord, &mock_point_list[7]);
        
        // Verify right-child address matches list address (a few samples)
        ASSERT_EQ(my_CBT_list.right_child(0).ptcoord, &mock_point_list[2]);
        ASSERT_EQ(my_CBT_list.right_child(2).ptcoord, &mock_point_list[6]);
        ASSERT_EQ(my_CBT_list.right_child(3).ptcoord, &mock_point_list[8]);
    }
    TEST_F(Fixture_CompleteBinaryTree, Verify_Complete_Binary_Tree_Property) {
        // Verify existence of left/right child node
        for (size_t i{}; i < ELEM_SIZE; ++i) {
            if (i <= 4)
                ASSERT_TRUE(my_CBT_list.has_left_child(i));
            else
                ASSERT_FALSE(my_CBT_list.has_left_child(i));
            if (i <= 3)
                ASSERT_TRUE(my_CBT_list.has_right_child(i));
            else
                ASSERT_FALSE(my_CBT_list.has_right_child(i));
        }
        
        // Verify tree height (a few samples)
        ASSERT_EQ(0, my_CBT_list.height(0));
        ASSERT_EQ(1, my_CBT_list.height(2));
        ASSERT_EQ(2, my_CBT_list.height(5));
        ASSERT_EQ(2, my_CBT_list.height(6));
        ASSERT_EQ(3, my_CBT_list.height(7));
        ASSERT_EQ(3, my_CBT_list.height(9));

        // Verify parent node (a few samples)
        ASSERT_EQ(KNN::MathVector(0),  *my_CBT_list.parent(0).ptcoord);
        ASSERT_EQ(KNN::MathVector(0),  *my_CBT_list.parent(2).ptcoord);
        ASSERT_EQ(KNN::MathVector(11), *my_CBT_list.parent(3).ptcoord);
        ASSERT_EQ(KNN::MathVector(22), *my_CBT_list.parent(5).ptcoord);
        ASSERT_EQ(KNN::MathVector(33), *my_CBT_list.parent(8).ptcoord);
        ASSERT_EQ(KNN::MathVector(44), *my_CBT_list.parent(9).ptcoord);
        
        // Verify left child node (a few samples)
        ASSERT_EQ(KNN::MathVector(11), *my_CBT_list.left_child(0).ptcoord);
        ASSERT_EQ(KNN::MathVector(55), *my_CBT_list.left_child(2).ptcoord);
        ASSERT_EQ(KNN::MathVector(77), *my_CBT_list.left_child(3).ptcoord);
        ASSERT_THROW((void)my_CBT_list.left_child(5).ptcoord, std::out_of_range);
            // use of (void) there was to silence "unused variable" warning

        // Verify right child node (a few samples)
        ASSERT_EQ(KNN::MathVector(22), *my_CBT_list.right_child(0).ptcoord);
        ASSERT_EQ(KNN::MathVector(66), *my_CBT_list.right_child(2).ptcoord);
        ASSERT_EQ(KNN::MathVector(88), *my_CBT_list.right_child(3).ptcoord);
        ASSERT_THROW((void)my_CBT_list.right_child(5).ptcoord, std::out_of_range);
            // use of (void) there was to silence "unused variable" warning
    }
} // END namespace Test_CompleteBinaryTree

namespace Test_BoundedVector {
    TEST(Test_BoundedVector, Simple_Verification) {
        std::mt19937_64 gen(23233.14115);
        std::uniform_int_distribution<size_t> dis1(1, 100);
        std::uniform_real_distribution<double> dis3(0.1, 2.0);

        KNN::BoundedVector simple_bounded (5);

        KNN::WavefrontObject wavefront_obj {R"(./data/grid_ptcld_10.obj)"};
        KNN::CBT_POD my_pod_mock;
        for (size_t i{}; i < wavefront_obj.get_point_count(); ++i) {
            my_pod_mock = {const_cast<KNN::MathVector*>(&wavefront_obj[i]), i};
            simple_bounded.push(my_pod_mock, wavefront_obj[i].norm());
        }

        size_t expected_ordered_values[] = {7,4,9,6,3};
        for (size_t i{}; i < simple_bounded.size(); ++i)
            EXPECT_EQ(expected_ordered_values[i], simple_bounded[i].ptnum);
    }
}

namespace Test_NearestNeighbor {
    struct Fixture_KNN : ::testing::Test {
        KNN::WavefrontObject wavefront_obj {R"(./data/grid_ptcld_10.obj)"};
//        std::chrono::milliseconds timer;
    };
    TEST_F(Fixture_KNN, Single_NN_Search) {
        KNN::NearestNeighbor knn_search {wavefront_obj};
        KNN::CBT_POD my_output_pod;

        // Verify closest point using a few, known samples.
        knn_search.search(my_output_pod, {0, 0, 0});
        EXPECT_EQ(7, my_output_pod.ptnum);
        knn_search.search(my_output_pod, {3, 0, 0});
        EXPECT_EQ(5, my_output_pod.ptnum);
        knn_search.search(my_output_pod, {-0.5, 0, -2});
        EXPECT_EQ(6, my_output_pod.ptnum);
        knn_search.search(my_output_pod, {2.5, 0.4, 2.5});
        EXPECT_EQ(0, my_output_pod.ptnum);
        knn_search.search(my_output_pod, {-2, 0, -3});
        EXPECT_EQ(1, my_output_pod.ptnum);
        knn_search.search(my_output_pod, {0.3, 0, 1.7});
        EXPECT_EQ(9, my_output_pod.ptnum);
    }
    TEST_F(Fixture_KNN, k_NN_Search_On_10_Points) {
        KNN::NearestNeighbor knn_bst {wavefront_obj};
        std::vector<KNN::CBT_POD> output;
        constexpr size_t k_value = 20; // will be clamped to max data size
        
        knn_bst.ksearch(output, {0, 0, 0}, k_value);
        
        constexpr size_t expected_ordered_values[] = {7,4,9,6,3};
        for (size_t i {}; i < 5; ++i)
            EXPECT_EQ(expected_ordered_values[i], output[i].ptnum);
    }
    TEST_F(Fixture_KNN, k_NN_Search_On_100k_Points) {
        cout << "\n";
        cout << "\t\t\tLoading 100,000 data points...";
        auto timer_start = std::chrono::high_resolution_clock::now();
        KNN::WavefrontObject wavefront {R"(./data/grid_ptcld_100000.obj)"};
        auto timer_end = std::chrono::high_resolution_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>
                        (timer_end - timer_start);
        cout << " Done!  (Elapsed " << elapsed.count() << " ms)\n";


        cout << "\t\t\tBuilding KD-Tree...";
        timer_start = std::chrono::high_resolution_clock::now();
        KNN::NearestNeighbor knn_bst {wavefront};
        timer_end = std::chrono::high_resolution_clock::now();
        elapsed = std::chrono::duration_cast<std::chrono::milliseconds>
                        (timer_end - timer_start);
        cout << " Done!  (Elapsed " << elapsed.count() << " ms)\n";


        cout << "\t\t\tKD-Tree height is "
             << knn_bst.height(knn_bst.size()) << endl;
        
        
        constexpr size_t k_value = 7;
        cout << "\t\t\tBegin searching for " << k_value << " nearest points.\n";
        std::vector<KNN::CBT_POD> output;
        timer_start = std::chrono::high_resolution_clock::now();
        knn_bst.ksearch(output, {0, 0, 0}, k_value);
        timer_end = std::chrono::high_resolution_clock::now();
        elapsed = std::chrono::duration_cast<std::chrono::milliseconds>
                        (timer_end - timer_start);


        constexpr size_t known_points[] =
                        {46276, 49048, 14294, 30254, 75774, 46991, 33633};
        for (size_t i {}; i < k_value; ++i) {
            cout << "\t\t\t\t [" << output[i].ptnum << "]  @  "
                 << *output[i].ptcoord << "\n";
            EXPECT_EQ(known_points[i], output[i].ptnum);
        }
        cout << "\t\t\t\tSearch time elapsed " << elapsed.count() << " ms\n";
        cout << "\n";
    }
} // END namespace Test_NearestNeighbor
