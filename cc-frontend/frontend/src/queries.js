import api from './api';

export const fetchDegrees = async () => {
    const { data } = await api.get('degrees/');
    return data;
};

/**
 * @param {object} props
 * @param {import('@tanstack/react-query').QueryKey} props.queryKey
 */
export const fetchDegreeBySlug = async ({ queryKey }) => {
    const [_key, slug] = queryKey;
    const { data } = await api.get(`degrees/${slug}/`);
    return data;
};

export const fetchMyEnrollments = async () => {
    const { data } = await api.get('degrees/my_enrollments/');
    return data;
};

