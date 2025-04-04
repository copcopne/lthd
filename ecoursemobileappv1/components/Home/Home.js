import { useEffect, useState } from "react";
import MyStyles from "../../styles/MyStyles"
import { ActivityIndicator, FlatList, Image, View, Text, TouchableOpacity } from "react-native";
import Apis, { enpoints } from "../../configs/Apis";
import { Chip, List, Searchbar } from "react-native-paper";
import { SafeAreaView } from 'react-native-safe-area-context';

const Home = () => {
    const[categories, setCategories] = useState([]);
    const[courses, setCourses] = useState([]);
    const[loading, setLoading] = useState(false);
    const[page, setPage] = useState(1);
    const[q, setQ] = useState();
    const[cateId, setCateId] = useState(null);

    const loadCates = async () => {
        let res = await Apis.get(enpoints["categories"]);
        setCategories(res.data);
    }

    const loadCourses = async () => {
        try {
            setLoading(true);

            let url = `${enpoints["courses"]}?page=${page}`;
            if (q) {
                url = `${url}&q=${q}`;
            }
            if (cateId) {
                url = `${url}&category_id=${cateId}`;
            }

            let res = await Apis.get(url);
            setCourses([...courses, ...res.data.results]);

            if(res.next === null)
                setPage(0);
        } catch {

        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadCates();
    }, []);

    useEffect(()=>{
        let timer = setTimeout(() => {
        loadCourses();
        }, 200);
        return () => clearTimeout(timer);
    }, [q, page, cateId]);

    const loadMore = () => {
        if(!loading && page > 0)
            setPage(page + 1)
    }

    return (
        <SafeAreaView style={[MyStyles.container, MyStyles.p]}>
            <Text style={MyStyles.subject}>DANH SÁCH KHÓA HỌC</Text>
            <View style={[MyStyles.r, MyStyles.w, MyStyles.m]}>

                <TouchableOpacity onPress={() => setCateId(null)}>
                    <Chip icon="label" style ={MyStyles.m}>Tất cả khóa học</Chip>
                </TouchableOpacity>
                
                {categories.map(c=> <TouchableOpacity key={c.id} onPress={() => setCateId(c.id)}>
                    <Chip icon="label" style ={MyStyles.m}>{c.name}</Chip>
                </TouchableOpacity>)}
            </View>

            <Searchbar
                placeholder="Tìm kiếm khóa học..."
                onChangeText={setQ}
                value={q}
            />

            <FlatList
                onEndReached={loadMore}
                ListFooterComponent={loading && <ActivityIndicator />}
                data={courses}
                renderItem={({ item }) => (
                    <List.Item
                        key={item.id}
                        title={item.subject}
                        description={item.created_date}
                        left={() => <Image style={MyStyles.avatar} source={{ uri: item.image }} />}
                    />
                )}
            />

        </SafeAreaView>
    );
}

export default Home;